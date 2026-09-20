---
id: KB-020
title: MiSTer porting oddity: ioctl_addr is one word past the last write when downloading ends
status: community-reported
confidence: medium
first_seen: 2026-09-20
last_verified: 2026-09-20
tags: [porting, mister]
applies_to: unspecified
sources:
  - https://github.com/agg23/analogue-pocket-utils/wiki/Porting
---

## Claim
MiSTer's ioctl_addr already points to the next address at the trailing edge of ioctl_downloading, so a file of size 0x100 shows ioctl_addr == 0x100 at the end, one higher than the last write. Cores that latch the size there need to subtract accordingly (or use a length counter).

## Evidence
agg23 wiki Porting page.

## How to validate on hardware
Not yet designed.
