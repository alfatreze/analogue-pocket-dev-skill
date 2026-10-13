---
id: KB-148
title: A Cyclone V fractional PLL has nine C counters, M/N/C values of 1 to 512, and all outputs divide one VCO within 600 to 1300 MHz on a -C8 part
status: docs-verified
confidence: high
first_seen: 2026-10-13
last_verified: 2026-10-13
tags: [pll,vco,fractional-pll,clocking,cyclone-v,quartus]
applies_to: Cyclone V E (5CEBA4F23C8, the Analogue Pocket FPGA), Quartus Prime Lite or Standard; Cyclone V Device Handbook Vol 1 as served on docs.altera.com, read 2026-10-13
sources:
  - Cyclone V Device Handbook Volume 1 (docs.altera.com), handbook ch.4: 4.2; datasheet PLL specifications
---

## Claim
PLL features table: nine output (C) counters, M, N and C sizes 1 to 512, a high/low-count pair per counter (each 1 to 256, their sum is the divide value), programmable duty cycle, and phase shift in steps of one eighth of the VCO period (125 ps at a 1000 MHz VCO). All outputs of one PLL divide a single VCO frequency; with several output frequencies the tool sets the VCO to a common multiple that is in range, then each C counter divides it down. There is an optional divide-by-two VCO post-divider. The datasheet VCO operating range is 600 to 1600 MHz for -C6, -C7 and -I7 speed grades and 600 to 1300 MHz for -C8 and -A7. The Pocket FPGA is a 5CEBA4F23C8, i.e. a -C8 part, so the usable ceiling is 1300 MHz (a footnote says the reported VCO frequency accounts for the post-divider, so the reported value can sit below the table figure when the post-divider is on).

## Evidence
PLL feature table (Table 24) and the counter descriptions in handbook 4.2; datasheet fVCO row and its footnote 53. The speed grade is read from the part number, not measured. This refines the 600 to 1600 MHz range quoted in the earlier PLL entry, which applies to faster grades.

## How to validate on hardware
Before adding an output frequency to a shared PLL, compute the common VCO for every output and compare against 1300 MHz for a -C8 part, not 1600 MHz. The Fitter's PLL summary shows the VCO it picked.
