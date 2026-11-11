---
id: KB-238
title: Large target read commands are about 1.6x faster than 4 KB ones, and a core can capture the data by bridge address
status: community-reported
confidence: medium
first_seen: 2026-11-09
last_verified: 2026-11-09
tags: [bridge,data-slots,sd-card]
applies_to: Analogue Pocket, openFPGA core issuing target (core-initiated) data-slot reads of a deferload file, Pocket firmware as of 2026-11, handheld
sources:
  - hardware test 2026-11-09
---

## Claim

A target read (command 0180) whose destination bridge address is in a window the core decodes itself (here the 0x4xxxxxxx range, never a core RAM address) is accepted, and the core sees every word as an ordinary bridge write; no length was refused up to 128 KB. The rate depends on the command length, not on the file: 4 KB commands run at about 0.96 MB/s once the first command after boot is out of the way, single commands of 16 KB, 64 KB and 128 KB at about 1.5 to 1.6 MB/s.

## Evidence

Hardware, 2026-11-09, handheld, one SD card: 4 KB 955 KB/s, 16 KB 1,562 KB/s, 64 KB 1,480 KB/s, 128 KB 1,571 KB/s. Every word was accepted (1,024; 4,096; 16,384; 32,768 words) with none dropped by a FIFO that absorbed the unstoppable bridge writes into SDRAM, and a 16 KB landing matched four separate 4 KB reads of the same file block for block. The first 4 KB command after boot took 10.3 ms (396 KB/s), later ones 4.2 ms. Not tested: lengths above 128 KB (a 1.7 MB picture is read as 14 commands of at most 128 KB), the dock, fragmented files, a second card.

## How to validate on hardware

Read the same 128 KB of a deferload file as one command and as 32 commands of 4 KB, time both with the core's free-running counter after a warm-up read, and compare the landed bytes with a normal read. Remember the CPU must read any buffer the bridge wrote through an uncached alias (see the entry on stale data caches).
