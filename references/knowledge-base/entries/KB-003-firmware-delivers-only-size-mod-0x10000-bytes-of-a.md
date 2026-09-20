---
id: KB-003
title: Firmware delivers only (size mod 0x10000) bytes of a nonvolatile slot of 64 KB or more
status: community-reported
confidence: medium
first_seen: 2026-09-20
last_verified: 2026-09-20
tags: [save, firmware, nonvolatile, limits]
applies_to: firmware version not stated by the source; re-test on current firmware
sources:
  - https://github.com/janisc/openfpga-NGPC/blob/main/target/pocket/core_top.v
---

## Claim
A nonvolatile slot whose size is >= 64 KB received only (size mod 0x10000) bytes (the file's tail): a 0x40200-byte slot received 0x200 bytes, deterministically, cold boot included. NGPC therefore keeps its save slot at 0xFE00 bytes.

## Evidence
NGPC core_top comment: 'Every probe agreed the firmware delivers exactly (size mod 0x10000) bytes of a nonvolatile slot'; the author notes no working core on their card had a save over about 64 KB. Not confirmed elsewhere; NES uses 0x40000 (256 KB) size table entries, which would contradict a universal limit, so scope and firmware version matter.

## How to validate on hardware
Create a nonvolatile slot with size_maximum 0x10200 and a known pattern file; log the bytes received by the bridge write path and compare with expected. Repeat below 0x10000. Record the firmware version.
