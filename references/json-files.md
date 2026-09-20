# Core definition JSON files (all fields, limits, gotchas)

All files: top-level object keyed by file type (`{"core":{...}}`, `{"data":{...}}`, `{"interact":{...}}`, `{"video":{...}}`, `{"input":{...}}`, `{"audio":{...}}`, `{"variants":{...}}`, `{"instance":{...}}`), each with `"magic":"APF_VER_1"`. Numbers may be ints or `"0x.."` strings. Required to run: core.json, data.json, interact.json, input.json, video.json, audio.json, variants.json (template ships all seven). Optional: info.txt (<=32 lines, shown in About), icon.bin.

## core.json
metadata: platform_ids (<=4, empty = standalone -> assets under `_none`), shortname<=31 (must match folder), description<=63, author<=31, url<=63, version<=31 (SemVer), date_release `YYYY-MM-DD`.
framework: target_product `"Analogue Pocket"`; version_required (`"1.1"`,`"1.2"`,`"2.0"`,`"2.1"`,`"2.3"`; bump when using newer features, e.g. 48-bit commands need 2.1); sleep_supported (sleep/save-state uses host 00A0/00A4); chip32_vm (<=15 chars, file at core folder root; takes over ALL loading); dock.supported (must be true), dock.analog_output (upcoming).
hardware: link_port; cartridge_adapter bitfield: bit31 leave cart power off; bit30 power always on; bit24 enable "Play Cartridge" in browser (skips slot 0 and slots deriving their name from it); bit17 strict adapter-ID check; bit16 soft check (only when Play Cartridge); [7:0] adapter id. 0 = power on, no checks; legacy -1 is mapped to 0x80000000.
cores[]: <=8 of {name<=15 optional, id, filename<=15 (the .rbf_r)}.
Doc sample has a typo (`"/"` instead of `"shortname"`); use `shortname`.

## data.json
data_slots[] <=32: name<=15, id (16-bit unique), required (missing -> file browser; false -> silently skipped), parameters (bitmap), nonvolatile (loaded at start, written back on core exit), deferload (no auto-load; size+ID still reported; use target read/write), secondary (only via instance/variant), filename<=31, extensions (<=4, <=7 chars, browser filter), size_exact, size_maximum, address (32-bit bridge load address).
Parameters bitmap: bit0 user-reloadable via Interact menu; bit1 core-specific (/Assets/<plat>/Author.Core/) vs platform common; bit2 filename cloned from slot 0 with this slot's first extension (saves); bit3 read-only; bit4 instance JSON (must also be core-specific, only valid in first slot); bit5 init nonvolatile with 0xFF up to size_maximum if file missing; bit6 send Reset Enter/Exit around a reload; bit7 restart whole core around reload (saves nonvolatile first); bit8 full reload incl. bitstream; bit9 persist browsed filename (cleared by "Reset All to Defaults"); [25:24] platform index into platform_ids for filename lookup. Example read-only+cloned-name = 4+8 = 12.
With Chip32: bit6 ignored; bit7 = soft reboot, chip32 re-runs with R0=slot id and must `HOST 0x4002` again.
Slot sample: save slot `parameters 7` (reloadable+core-specific+cloned name), size_maximum 8192, address 0x02000000.
Nonvolatile write-back happens on Quit/power off/sleep, with the size taken from the 0x2000 table; the 1.1 beta 5 changelog added logging explaining why a slot was not saved (enable Debug Logging).

## interact.json
`variables[]` <=16 items (list options don't count). Common: name<=23, id (unique, 16-bit; persistence is matched by id across updates), type, enabled, address (32-bit bridge). Types: `radio` (group), `check`, `slider_u32` (graphical{signed,min,max,adjust_small,adjust_large}), `list` (options<=16 {value,name}), `number_u32` (read-only hex display), `action` (one-shot write of `value`).
Optional: persist, writeonly (skip read-back), defaultval, value, value_off (default 0; written when unchecked), mask (read-modify-write: bits SET in mask are left untouched, bits clear are modified).
Persistence: `/Settings/Author.Core/Interact/interact_persist.json`; per-asset menus (matched to the slot-0 asset path) persist to `/Settings/Author.Core/Interact/<slot0 asset path>.json` and presets to `/Presets/...`. Persisted values are written into the core register space at boot immediately before Reset Exit, and saved/read at shutdown (after Reset Enter). Per-asset menu overrides the core menu. Data slots flagged reloadable appear in the menu for runtime reload. Interact writes go to bridge addresses you decode (e.g. 0x00F0000C in the example).

## video.json
scaler_modes[] <=8 {width,height,aspect_w,aspect_h,dock_aspect_w/h optional,rotation 0/90/180/270,mirror bit1=LR bit0=UD}; display_modes[] <=16 {id}; defaults{sharpness 0-3}. Core switches scaler slot at runtime via end-of-line bits.
Display mode IDs: 0x10 CRT Trinitron; 0x20 Grayscale LCD (generic), 0x21 GB DMG, 0x22 GBP, 0x23 GBP Light (0x20-0x23 need grayscale + 0x444D response to 00B8); 0x30 Reflective Color LCD, 0x31 GBC, 0x32 GBC+; 0x40 Backlit Color LCD, 0x41 GBA, 0x42 GBA SP 101; 0x51 GG, 0x52 GG+; 0x61 NGP, 0x62 NGPC, 0x63 NGPC+; 0x71 TurboExpress, 0x72 PC Engine LT; 0x81 Lynx, 0x82 Lynx+; 0xE0 Pinball Neon Matrix, 0xE1 Vacuum Fluorescent. Prefer generic modes over "Original" ones. Trinitron needs no horizontal pixel duplication and only works for scaler slot 0 with multiple rotations; if no display_modes are listed and height is 200-400, Trinitron auto-unlocks.

## input.json
controllers[] <=4 {type:"default", mappings[] <=8 {id, name<=19, key}} with keys pad_btn_a/b/x/y, pad_trig_l/r, pad_btn_start, pad_btn_select. Per-asset mappings supported (1.1 beta 3); users can remap (beta 5) if input.json exists.

## audio.json
Only `magic` today (upcoming feature).

## variants.json (upcoming)
variant_list <=8 {name<=15,id,core_select{core_id},data_override[]<=8,memory_writes[]<=16}. Field naming is inconsistent in the docs (text says data_id_to/data_id_from, sample uses data_id/data_id_override). Prefer instance JSON, which is what the 1.1 beta 7 changelog moved to.

## <instance>.json
Loaded by a slot 0-type data slot with bit4 set and extension `json`. Fields: data_path (<=255, forward slashes, relative base folder), core_select{id,select} (choose among up to 8 bitstreams), data_slots[] <=32 {id, filename<=255 relative to instance location, no `..`}, memory_writes[] <=32 {address,data} applied during boot before slots load (variant + instance total 16+16 per boot doc).
