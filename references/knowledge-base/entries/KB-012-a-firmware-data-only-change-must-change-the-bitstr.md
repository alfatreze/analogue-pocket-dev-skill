---
id: KB-012
title: A firmware/data-only change must change the bitstream hash, or the build did nothing
status: community-reported
confidence: medium
first_seen: 2026-09-20
last_verified: 2026-09-20
tags: [process, build, verification]
applies_to: process lesson from one project
sources:
  - https://github.com/thekoalakoa/paprium-pocket/blob/master/docs/BUILD_REFERENCE.md
---

## Claim
When firmware or memory-init files feed Quartus via $readmemh, a rebuild without copying the new file uses the old firmware. Identical fit metrics plus identical bitstream md5 means the build is void; timing reports cannot tell you.

## Evidence
Paprium BUILD_REFERENCE 'A firmware-only change must CHANGE THE BITSTREAM'.

## How to validate on hardware
After every firmware/init change compare sha256 of the .rbf and installed .rbf_r against the previous build and against the card.
