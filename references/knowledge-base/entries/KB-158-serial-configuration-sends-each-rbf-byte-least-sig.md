---
id: KB-158
title: Serial configuration sends each .rbf byte least-significant bit first, so a loader that expects the other bit order needs a bit-reversed file
status: docs-verified
confidence: medium
first_seen: 2026-10-13
last_verified: 2026-10-13
tags: [configuration,rbf,bit-order,passive-serial,cyclone-v]
applies_to: Cyclone V E (5CEBA4F23C8, the Analogue Pocket FPGA), Quartus Prime Lite or Standard; Cyclone V Device Handbook Vol 1 as served on docs.altera.com, read 2026-10-13
sources:
  - Cyclone V Device Handbook Volume 1 (docs.altera.com), handbook ch.7: 7.9
---

## Claim
In passive serial configuration with .rbf, .hex or .ttf data, the least-significant bit of each byte is sent first; the handbook's example turns the bytes 02 1B EE 01 FA into the serial stream 0100-0000 1101-1000 0111-0111 1000-0000 0101-1111 on DATA0. A host that streams the file bit by bit must follow that order. The handbook does not mention any bit-reversed file format, so it neither confirms nor explains why a platform loader may ask for a reversed copy of the raw .rbf; any such requirement is the platform's own convention.

## Evidence
Section 7.9 of the handbook (the byte example). No statement in the handbook about reversed bitstream files was found. Treat the bit-order rule as documented for passive serial only; the FPP section does not restate it in the text used here.

## How to validate on hardware
Compare a raw .rbf and the platform's reversed file byte by byte with each byte's bits reversed (a short script); a match means the platform loader applies this same LSB-first rule on its side, which is the usual reason for the second file.
