# SD layout, packaging, assets, debugging aids

## SD structure
- `/Cores/Author.Core/` (name must equal core.json author.shortname): 7 json, bitstream `.rbf_r`, optional icon.bin/info.txt/chip32 .bin.
- `/Platforms/<shortname>.json` (+ `_images/<shortname>.bin`): platform shortname = lowercase a-z0-9_, <=15 chars, not starting with `_`. Fields category<=31, name<=31, manufacturer<=31, year (int). Missing platform json => no platform info or future features; cores also disappear from the openFPGA menu if json is invalid (check Tools > Developer > Builds).
- `/Assets/<platform>/common/` (shared), `/Assets/<platform>/Author.Core/` (core-specific), `/Assets/_none/Author.Core/` (standalone). `/Saves/...` mirrors Assets (nonvolatile slots; create subfolders automatically). `/Settings/Author.Core/Interact/` persisted interact values; `/Presets/` per-asset interact; `/Memories/Beta/author.core/` (128 per core; savestates/screenshots); `/System/` (Logs, Library images); `/GB Studio/`.
- Zip may contain only Pocket-created base folders; name `Author.Core_Version_YYYY-MM-DD.zip`; extract at SD root.

## Bitstream
Quartus `.rbf` -> `.rbf_r` by reversing bits in every byte (C tool in `docs-snapshot/packaging-a-core.txt`; a 5-line Python `int('{:08b}'.format(b)[::-1],2)` equivalent works). Quartus settings if not from template: output dir `output_files`, Programming Files: Raw Binary File (.rbf), "Generate compressed bitstreams" on. `.sof` is for JTAG only. Template `.qsf` was generated with Quartus Prime 18.1.1 Lite (Cyclone V). Getting-started requires Quartus Lite with Cyclone V support and an Intel-approved USB/Ethernet Blaster (clones discouraged).

## Development loop
Copy a working bitstream.rbf_r into /Cores/... once; afterwards load `.sof` over JTAG and Pocket automatically repeats the whole boot (heartbeat loss detection). USB-C SD access (~700 KB/s; Analogue+X attach / Analogue+Y detach since 2.1) or SD card swap for JSON/asset changes. Never remove the battery.

## Debugging aids (Tools > Developer)
Builds list; USB SD Access; Statistics overlay (power on dev units, temperature, refresh rate to 3 decimals, sync ok/low/high; falls back to internal 60 Hz if sync missing); Pause Core Boot (halts after bitstream load, A continues host handling); Pause Load Data (arm SignalTap before slot loads); Asset Load Detail (files <512 KB may flash by); Debug Logging -> `/System/Logs/<author>.<core>_<timestamp>.txt` including why a nonvolatile slot was not saved; Chip32 Exec Log. Only the first two options persist across power cycles. Force power-off: undock, hold power 5 s (loses unsaved saves).

## Graphics
- Core icon `icon.bin`: 36x36 monochrome, 16-bit pixels (brightness in upper byte, 0xFF00 = on), stored rotated 90 deg CCW.
- Platform image: 521x165 (WIP), `.bin` same family of formats.
- Library images `/System/Library/Images/<platform>/<crc32>.bin`: header magic LE `0x41504910` (RGB16) or `0x41504920` (RGB32) + width u16 + height u16; pixels rotated 90 deg CCW, BGRA bytes with alpha 0xFF; filename = lowercase CRC32 of the game (for multi-file games: CRC32 of files concatenated alphabetically, deepest folder first).
- GB palettes `/Assets/gb/common/palettes/*.pal`: exactly 56 bytes: BG, OBJ0, OBJ1, Window (4 x RGB24 each = 48 B), LCD-off color (3 B), footer `81 41 50 47 42` ("\x81APGB"). Loaded via Settings > Pocket > Systems > GB > Video > Color Palettes > Custom.
