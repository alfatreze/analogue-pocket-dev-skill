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
