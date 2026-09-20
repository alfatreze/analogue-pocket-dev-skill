# Host/Target commands, memory map, structs (complete)

Source: developer/docs/host-target-commands. Verified against `open-fpga/core-template` `core_bridge_cmd.v`.

## Memory map (BRIDGE, base 0xF8000000; all 0xF8xxxxxx reserved)
| Addr | R/W (H=host, T=target) | Purpose |
|---|---|---|
| 0x0 | R:H,T W:H,T | Host command/status |
| 0x4 | R:H W:T | Host param pointer (address where Pocket writes params; template default 0x20) |
| 0x8 | R:H W:T | Host response pointer (template default 0x40) |
| 0x1000 | R:H,T W:H,T | Target command/status |
| 0x1004 | R:H W:T | Target param pointer |
| 0x1008 | R:H W:T | Target response pointer |
| 0x2000-0x20FF | R/W both | Data slot ID/size table, 32 x 8 bytes |
| 0x2380-0x238B | R:H | Build date BCD (0x20220531), time BCD (0x00231159), unique ID (Tcl-generated `build_id_gen.tcl`) |

Template BRAM-less layout: host params 0x20..0x2C, host response 0x40..0x4C, target params 0x1020.., target response 0x1040...

### Data slot ID/size table
Per entry: Word0 `[15:0]` slot ID (json id), Word1 `[31:0]` size in bytes (0 = unused). Pocket writes the loaded file size; core may change it (esp. nonvolatile save files). Pocket reads it back on flush/shutdown and resizes the SD file. For deferload slots ID+size are still written. >4 GB files: Word0 `[31:16]` = size bits 47:32.

## 3-stage handshake
Host: `0x434D 'CM'`+cmd (Pocket writes) -> `0x4255 'BU'`+progress (core) -> `0x4F4B 'OK'`+result (core).
Target: `0x636D 'cm'`+cmd (core writes) -> `0x6275 'bu'` (Pocket) -> `0x6F6B 'ok'`+result (Pocket).
Template returns `OK` + `0xFFFF` for an unknown host command.

## Host commands (Pocket -> core)
| Code | Name | Params | Response | Result codes |
|---|---|---|---|---|
| 0x0000 | Request status | 0 | 0 | 0 undefined, 1 booting (PLLs/FSMs), 2 setup (assets loading, core may request slot reads), 3 idle (held in reset), 4 running |
| 0x0010 / 0x0011 | Reset enter / exit | 0 | 0 | - |
| 0x0080 | Data slot request read | slot id | 0 | 0 ready, 1 never allowed, 2 check later |
| 0x0082 | Data slot request write | [15:0]+[31:16] slot id / size hi; [31:0] size lo | 0 | same as 0x0080 |
| 0x008A | Data slot update | slot id, size | 0 | 0 |
| 0x008F | Data slot access all complete | 0 | 0 | 0 |
| 0x0090 | Real-time clock | epoch secs; BCD date 0x20221031; BCD time 0x00235959 with [27:24] day of week (added 2.0) | 0 | sent once at boot |
| 0x00A0 | Savestate start/query | [0] request start | 3: [0] supported, addr, size | 0 ok/no op, 1 busy, 2 done, 3 error |
| 0x00A4 | Savestate load/query | [0] request load | 3: [0] supported, addr, max size | same |
| 0x00B0 | OS notify: menu state | [0] in menu | 0 | optional |
| 0x00B1 | OS notify: cartridge adapter | [24] Play Cartridge chosen, [16] cart power on after reset exit, [7:0] adapter id 0x01-0x04 | 0 | always sent, while core in reset |
| 0x00B2 | OS notify: docked | [0] docked | 0 | |
| 0x00B8 | OS notify: display mode | [15:8] mode id, [0] grayscale-only required | 1: [15:0] must be 0x444D to permit grayscale LCD modes | added 2.0 |

## Target commands (core -> Pocket)
| Code | Name | Params | Results |
|---|---|---|---|
| 0x0140 | Ready to run | 0 | - |
| 0x0152 | Debug event log | [31:0] event id (timestamped in debug log) | - |
| 0x0180 | Data slot read | [15:0] slot, [31:0] slot offset, [31:0] bridge addr, [31:0] length | 0 ok, 1 slot undefined, 2 error/out of range (length 0xFFFFFFFF = clamp to max legal) |
| 0x0181 | Read 48-bit | [31:16] offset hi + [15:0] slot, offset lo, addr, length | same (needs framework 2.1) |
| 0x0184 | Data slot write | as 0x0180 | 0 ok, 1 undefined, 2 error |
| 0x0185 | Write 48-bit | as 0x0181 | same |
| 0x0188 | Data slot flush | [15:0] slot | 0 written, 1 undefined |
| 0x0190 | Get filename of slot | slot, pointer to `get_dataslot_file_t` | 0 ok, 1 undefined |
| 0x0192 | Open new file into slot | slot, pointer to `open_dataslot_file_t` | 0 opened, 1 created+opened, 2 slot undefined, 3 not found, 4 malformed path, 5 general error |
Boot doc also references `[0182 Data slot copy]` (core asks Pocket to load a different slot next); it is not in the command list, so treat as unverified.

## Structs
`get_dataslot_file_t`: 0x0, 256 bytes, NUL-terminated full path, e.g. `/Assets/abcd/common/directory1/data.bin`.
`open_dataslot_file_t`: 0x0 path (256 B, Assets or Saves, any platform the core supports); 0x100 flags (bit0 create if missing, bit1 resize/truncate; slot must not be read-only); 0x104 desired size.

## Behavioral notes
- Target read/write are meant for slots with `deferload`; APF still updates the size table. User-reloadable deferload slot -> Pocket sends only 0x008A (not 0082/008F).
- APF caches open file + up to 16 fragments per slot; switching slots between target ops discards the cache (slow re-seek in dense directories). 1.1 added open/seek caching; 2.1 fixed length 0xFFFFFFFF; 2.3 fixed 0192 size fields; beta 7 fixed a 0184 truncation bug.
- Files > 4 GB need exFAT and `framework.version_required >= 2.1`.
- Nonvolatile slot is written back to SD at core shutdown (Quit, power off, sleep) using the size in the ID/size table; see data-json notes.
- **Template gap (verified in source):** `core_bridge_cmd.template.v` target FSM only issues 0x0140, 0x0180, 0x0184, 0x0190, 0x0192. It does NOT implement 0x0181, 0x0185, 0x0188 or 0x0152. Cores wanting flush/48-bit/debug-log must add the state machine themselves; a core that writes 0x6C6D_0188 with no other changes is testing an unimplemented-in-template path, and the public docs do not prove what Pocket does with it beyond the result table.
- Bridge reads are buffered: the core may return read data up to the *next* read strobe (one-beat lag is legal), so bridge read muxes must tolerate data arriving late.
