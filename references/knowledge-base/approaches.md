# Approaches, workarounds and design patterns seen in real cores
Status labels follow the knowledge-base ladder. Everything here is a lead unless it cites an entry that is validated.

1. **Claim the save size from the core (KB-001).** Continuously write `has_save ? size : 0` (NES) or a fixed size once a save exists (NGPC) into the size-table entry of the save slot's *position*. Simplest fix for "save file never appears".
2. **Persist only what changed (NGPC).** Track dirty flash blocks, stage them in PSRAM, CRC-bind to the cartridge identity, apply before boot, flush through a demuxed bridge-read region. Trades MiSTer .sav compatibility for a sub-64 KB slot (see KB-003).
3. **Carry the cartridge inside the savestate (NGPC).** Embed the save image in the savestate blob so Memories/sleep rewind machine and cart atomically (96 KB states).
4. **Soft-CPU as bridge master.** LiteX RISC-V (agg23), NEORV32 (Paprium), Neogeo Overdrive's soft CPU: run firmware that owns the file API, interact registers and asset handling, instead of hard FSMs. Lets you iterate on load/save logic without a 25-minute fit; interact entries can be mapped to a register window (LiteX: 0x1000_0100..0x1000_013C = indices 0-15 with a changed-flag per entry).
5. **UART/JTAG over the dev cart or USB Blaster.** Devkit cart gives 2 Mbps UART for logs and program hot-reload without touching SD (needs cartridge_adapter 0). A JTAG UART works with a genuine Blaster.
6. **Split bitstreams + Chip32 chooser.** Big cores ship several bitstreams (PAL/NTSC, system variants, SNES chips) and let a Chip32 program or `<instance>.json core_select` pick one, instead of runtime PLL reconfig (KB-015).
7. **Deferload + target commands for big or dynamic data.** Keep ROMs on the SD card and stream on demand with 0180 (`data_loader`-style consumption); watch the per-slot file cache (switching slots discards it).
8. **Chip32 emulator loop.** agg23's `openfpga-chip32-sim` lets Chip32 loaders be tested on a PC before hardware.
9. **Reduce fit risk with discipline (KB-011/KB-012).** Archive every fit report and bitstream hash, re-seed 3-4 times, gate on setup/TNS/hold plus a boot smoke test rather than ALM count, and confirm the bitstream actually changed after firmware-only edits.
10. **Firmware-config through interact.json.** Persisted interact values are written into core registers before Reset Exit and are the one documented persistence path that needs no core-side file handling.
11. **Multi-bit CDC done right.** Use `sync_fifo.sv` from analogue-pocket-utils for buses; keep single-bit `synch_3` for flags (KB-009).
12. **Audio/data IP reuse.** `sound_i2s.sv` (I2S, FIFO sync, signed/unsigned), `data_loader.sv`/`data_unloader.sv` (bridge <-> byte/word memory), `psram.sv` (Pocket-timed PSRAM), `hex_loader.v`, `debug_key.v`.
13. **Declare an `address` on the nonvolatile save slot and serve bridge reads there (KB-004).** NGPC, K3V GBA and openfpgaSDK all do; use ready/valid handshakes rather than a fixed-latency `data_unloader` over variable-latency memory (KB-026).
