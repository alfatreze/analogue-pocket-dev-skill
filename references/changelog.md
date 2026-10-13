# openFPGA / APF changelog digest (framework versions gate features)
Pages: developer/docs/changelog/{1-1-beta-1,3,4,5,6,7,1-1,1-2,2-0,2-1,2-3}. Full text in `docs-snapshot/changelog__*.txt`. (No 2.2 page exists.)

- 1.1 beta 1: interact.json (custom settings menu), input.json, platform category, info.txt + author icon, menu-state host command 00B0, memories dir, data slot reload via interact, fixed save bug with param bit 5.
- beta 3: per-asset controls mapping, checkbox `value_off`, instance memory writes 8->16, "Pause Core Boot" option, fixed nonvolatile-reload data loss and dock rotation.
- beta 4: Chip32 VM, debug logging, asset detail tool, `list` interact type, interlaced video, controller connection type bits, dock analog sticks, expected size reporting, fix: 0082 passes size first.
- beta 5: user remapping of input, platform grouping, Chip32 fixes (reinit via JTAG, LOADF issues Request Write and honors ADJFO, cycle limit), logging explains unsaved slots, B halts Chip32.
- beta 6: screenshots/memories images, first large-file target commands (0180/0184), keyboard/mouse in dock (players 3/4), host 008A, RTC host 0090 + GETTIME, deferload support.
- beta 7: Library, screenshots, instance `core_select` (up to 8 bitstreams, replaces variant_select), instance memory writes 32, param bit 9 (persist browsed filename), fixed 0184 truncation bug.
- 1.1: target 0190 get filename, 0192 open new file; faster target servicing; open/seek caching (esp. FAT32).
- 1.2: version_required "1.2"; cartridge adapter support (core.json cartridge_adapter, host 00B1, Play Cartridge), cartridge line audio on I2S ADC, host 00B2 docked state, target 0152 debug event log, slot can load from another platform's Assets (param bits 25:24 + filename).
- 2.0: all display modes usable, CRT Trinitron, host 00B8 display mode (0x444D grayscale response), dock-only aspect ratios, day-of-week in 0090.
- 2.1: 48-bit offsets/sizes: target 0181/0185, 0082/008A/BRAM sizes 48-bit; fixed length 0xFFFFFFFF; files >4 GB need exFAT; USB SD hotkeys; Builds list remembers selection.
- 2.3: display modes for NGP, NGPC, TG16, Lynx and Vacuum Fluorescent; fixed 0192 not updating slot size fields.

## Pocket OS firmware after framework 2.3 (no new framework version; checked 2026-09-29)
- 2.6.0 (2026-06-17): openFPGA "Recent" category; quitting a core returns to the openFPGA menu; cached openFPGA menu opens faster. OS Auto Dim / Auto Off power options (idle dimming is an OS function). KB-072.
- 2.7 (2026-09-04): higher maximum platform/core count; pre-cached core lists load twice as fast; unplugging USB while a core runs no longer unstable. KB-072.
- Docs site (2026-09): the openFPGA developer docs moved to `/developer/docs/openfpga/...` (old URLs 308-redirect) with no text change; new `/developer/docs/api` (public firmware-list API) and `/developer/docs/platform` (Analogue 3D only).

## Skill additions (not framework changes)
- 2026-10-13, weekly refresh: Analogue developer docs unchanged; Cyclone V Quartus edition chart unchanged (Lite yes, Standard yes, Pro no); three watched community repos advanced (NGPC, GBA, library metadata); Codeberg tutorials still unreachable.
- 2026-10-13, eight project-derived entries made general and promoted to the public set: KB-056 (catalog caches after a file-drop install), KB-060 (vsync pulse too short to poll), KB-079 (interact.json 16-entry cap), KB-080 (data.json reload bit), KB-081 (shared PLL VCO), KB-082 (CDC timing without JTAG), KB-103 (screenshots as a lossless data channel), KB-126 (TRS plug into a balanced input records left minus right).
- 2026-10-13, Cyclone V silicon reference: `scripts/fetch_cyclone_docs.py` fetches the Device Handbook Volume 1, Datasheet, Overview, GX/GT/E errata and two older PDFs into the git-ignored `references/docs-snapshot/cyclone-v/`. Paraphrased, docs-verified entries KB-143 to KB-166 by topic: embedded memory and MLAB inference (143-146), DSP block (147), PLL and clocking (148, 150), errata (149), I/O banks, levels, IOE controls and registers (151-154), external-memory scope (155), configuration and reset after configuration (156-158), power-on reset and hot-socketing (159-160), CRC error detection and JTAG boundary-scan (161-164), logic array blocks and ALM modes (165-166).
- Corrections made on the way: the PLL VCO ceiling is 1300 MHz on a -C8 part (the Pocket's 5CEBA4F23C8), not the 1600 MHz of faster grades (KB-148 refines KB-081); MLAB read-during-write is wider than "old data only" (KB-144); 18 x 18 multiplier count on the A4 is 132 (66 blocks, two per block), not 66 (KB-147).
