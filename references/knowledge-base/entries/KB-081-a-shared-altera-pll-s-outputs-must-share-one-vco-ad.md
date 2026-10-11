---
id: KB-081
title: A shared altera_pll's outputs must share one VCO -- adding an incompatible frequency fails synthesis, not timing
status: hardware-validated
confidence: high
first_seen: 2026-09-30
last_verified: 2026-09-30
tags: [altera-pll, pll, clock-generation, quartus, cyclone-v, fitter-error, local-technique]
applies_to: any Cyclone V (or similar Intel/Altera fPLL) design adding a new output clock to an
  existing multi-output altera_pll instance
evidence: A 5th PLL output at 12.288 MHz added to a shared altera_pll failed Fitter with an "illegal value" error. Fixed with a second independent PLL instance; a synthesis-only quartus_map run then reported "Implemented 5 PLLs", and a full fit closed timing on both seeds.
sources:
  - Intel Quartus altera_pll documentation (output counters divide one VCO)
---

## Claim
All outputs of a single `altera_pll` instance divide from ONE VCO frequency via integer output
counters. Before adding a new output frequency to an existing shared PLL, check whether a common VCO
exists that integer-divides into EVERY requested output (existing + new) within the device's legal VCO
range (roughly 600 MHz-1600 MHz for Cyclone V fPLLs) -- not just whether the new frequency "sounds
reasonable" on its own. If no such VCO exists, Quartus's Fitter will reject the new output as an
"illegal value" with a hard error (not a timing-margin warning), and the only fix is a second,
independent `altera_pll` instance for the incompatible frequency, taking the same reference clock.

## Evidence
One core's shared PLL already produced 66.667/60 MHz (CPU), 12.000 MHz x2 (video), and 100.000 MHz
(SDRAM) from a 600 MHz VCO (integer counters 9/10, 50, 50, 6). Adding a 5th output at 12.288 MHz (an
I2S audio MCLK) failed: `Error: PLL Output Counter parameter 'output_clock_frequency' is set to an
illegal value of '12.288 MHz'`. Solving for the smallest VCO frequency that integer-divides into ALL
FIVE targets simultaneously gives 38,400 MHz (LCM in Hz) -- physically impossible for this PLL family.
clk_sys's own frequency (60 vs 66.667 MHz) was NOT the limiting constraint in this case; the fixed
video (12 MHz) and SDRAM (100 MHz) clocks were. Fix: a second, standalone `altera_pll` instance with
its own `number_of_clocks(1)`, same reference clock input, producing only the incompatible frequency --
confirmed via a cheap synthesis-only `quartus_map` run before spending a real fit ("Implemented 5
PLLs", 0 errors), then a full fit closed timing cleanly on both seeds with the extra PLL instance.

## How to validate on hardware / before spending a Quartus fit
Before adding a new output frequency to a shared PLL: compute the LCM (in Hz, exact integers, not
rounded MHz) of every existing output frequency plus the new one. If that LCM exceeds the device's
real VCO range, the new frequency cannot share this PLL -- design a second PLL instance for it from
the start, rather than discovering the Fitter error after a wasted compile. A synthesis-only
`quartus_map` run (a few minutes, no fit) is enough to confirm the new PLL resource is actually
available on the device/pin-lock region before committing to a real multi-seed fit.
