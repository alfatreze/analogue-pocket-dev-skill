---
id: KB-015
title: PLL dynamic reconfiguration is unreliable with the 74.25 MHz source; ship separate bitstreams
status: community-reported
confidence: medium
first_seen: 2026-09-20
last_verified: 2026-09-20
tags: [pll, clocks, video]
applies_to: observed on SNES port
sources:
  - https://github.com/agg23/analogue-pocket-utils/wiki/PLL-Reconfig
---

## Claim
Reconfiguring for PAL/NTSC works imperfectly because two undocumented variables (prst, ph_mux_prst) change and cannot be set; clocks come out slightly offset. Recommended workaround: build separate PAL/NTSC bitstreams (and use Chip32 or an instance JSON to choose).

## Evidence
agg23 wiki PLL Reconfig page and SNES port experience.

## How to validate on hardware
Measure output frequency after reconfig with a counter against clk_74a.
