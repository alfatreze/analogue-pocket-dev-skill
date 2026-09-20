---
id: KB-014
title: Pocket video pitfalls: zeros outside DE, HS 3+ cycles after VS, mid-HS VS can wedge the scaler
status: community-reported
confidence: medium
first_seen: 2026-09-20
last_verified: 2026-09-20
tags: [video, scaler]
applies_to: firmware 1.1-beta-3 era report; re-check on current firmware
sources:
  - https://github.com/agg23/analogue-pocket-utils/wiki/Video
---

## Claim
vidout_rgb must be 0 when DE is low: the values just before the first and after the last DE pixel configure the scaler. VS/HS must be one-cycle pulses, HS at least 3 cycles after VS. Porches need not be accurate. Some arcade cores with VS in the middle of an HS pulse hard-crashed the scaler so no core produced video until a full power cycle. Very small resolutions can drop pixels (integer-scale yourself). Internal panel is RGB565; dock output 21-bit.

## Evidence
agg23 wiki Video page; official Bus Communication timing rules agree on most points.

## How to validate on hardware
If video disappears across cores, power-cycle the Pocket before debugging further.
