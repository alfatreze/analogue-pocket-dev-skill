---
id: KB-240
title: A soft CPU data cache serves stale bytes of a buffer the bridge wrote: read it through an uncached alias
status: community-reported
confidence: medium
first_seen: 2026-11-09
last_verified: 2026-11-09
tags: [cpu,cache,bridge,data-slots]
applies_to: openFPGA core with a soft RISC-V CPU (VexRiscv with 4 KB instruction and data caches, cacheability chosen by address bit 31) whose on-chip RAM also receives target-read data from the bridge, Pocket firmware as of 2026-11
sources:
  - hardware test 2026-11-09
---

## Claim

When the bridge (a target read) writes into core RAM behind the CPU's back, the CPU's data cache keeps the lines of the previous read at the same address: a second read of different file bytes into the same buffer is seen as the first one's data. The fix is to read such a buffer through an uncached alias of the RAM (here address + 0xC0000000); writing the destination through the physical address is fine.

## Evidence

Hardware, 2026-11-09: a test read file block 0 and then block 1 into the same 4 KB buffer and compared the buffer with data landed elsewhere. Reading through the ordinary address gave block 0's data for block 1 (the compared words differed in 991 of 1,024 positions, 32 matched by chance), so a correct landing was reported as damaged; reading through the uncached alias gave an exact match and a "0123 OK" block map. Found by looking up the first mismatching word in the file offline: the "bad" word was the correct word of the second block.

## How to validate on hardware

Read two different blocks of a file into one buffer, checksum the buffer through the cached and the uncached address after each, and compare with a host checksum of the file; the cached view repeats the first block.
