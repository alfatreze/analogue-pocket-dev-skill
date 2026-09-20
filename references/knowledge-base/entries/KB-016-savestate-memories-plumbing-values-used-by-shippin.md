---
id: KB-016
title: Savestate/Memories plumbing values used by shipping cores
status: source-verified
confidence: high
first_seen: 2026-09-20
last_verified: 2026-09-20
tags: [savestate, sleep, memories]
applies_to: framework 1.1-2.3
sources:
  - https://github.com/agg23/openfpga-NES/blob/main/target/pocket/core_top.v
  - https://github.com/janisc/openfpga-NGPC/blob/main/target/pocket/core_top.v
  - https://www.analogue.co/developer/docs/host-target-commands
---

## Claim
Cores expose `savestate_supported`, `savestate_addr` (a bridge address where the state blob lives), `savestate_size` and `savestate_maxloadsize`. NES uses addr 0x40000000, size 0x144008, max load size + 0x1000 ('extra data we will just discard'). NGPC uses 98720 bytes and embeds the cartridge save image in the state. Sleep/wake depends on savestates: cores without them report sleep unsupported.

## Evidence
NES and NGPC core_top source; agg23 (issue 59 on openfpga-SNES) says the implementation 'took a lot of trial and error' and is generally copied by others; the NES release notes call it a 100-hour effort ending in a single-line fix.

## How to validate on hardware
Trigger Memories on the reference NES core to see the 00A0 query then start handshake in a debug log before implementing your own.
