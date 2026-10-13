---
id: KB-147
title: The variable-precision DSP block gives 66 blocks on the 5CEBA4: one 27 x 27, two 18 x 19 or three 9 x 9 multipliers each, with a hard pre-adder and 64-bit accumulator
status: docs-verified
confidence: high
first_seen: 2026-10-13
last_verified: 2026-10-13
tags: [dsp,multiplier,cyclone-v,inference]
applies_to: Cyclone V E (5CEBA4F23C8, the Analogue Pocket FPGA), Quartus Prime Lite or Standard; Cyclone V Device Handbook Vol 1 as served on docs.altera.com, read 2026-10-13
sources:
  - Cyclone V Device Handbook Volume 1 (docs.altera.com), handbook ch.3: 3.1 to 3.6
---

## Claim
Each block supports 9-, 18- and 27-bit word lengths. Per block the independent modes give three 9 x 9, two 18 x 18 or 18 x 19, one 18 x 25, one 20 x 24 or one 27 x 27 multiplier; further modes are two 18 x 19 multipliers summed, 18 x 18 summed with a 36-bit input, and complex 18 x 19 over two blocks. The 5CEBA4 (A4) lists 66 blocks in the resource table (so 66 27 x 27, 132 18 x 18 or 198 9 x 9 independent multipliers). Other features: a hard pre-adder (19- and 27-bit modes, for symmetric filters), an internal coefficient register bank, a 64-bit accumulator with double accumulation, a chain-out adder and cascade paths for systolic FIR. Restrictions: the pre-adder needs all inputs and multipliers on the same clock, and input cascade is unavailable while the pre-adder is on. Blocks can be reached by the Quartus DSP IP cores or by HDL inference.

## Evidence
Features (3.1), supported modes (Table 14), resources (Table 15 for the A4 row) and design considerations (3.4) in the handbook chapter. The 66-block figure matches the DSP count the project's Quartus reports show as the device total.

## How to validate on hardware
In the Quartus fit report look at the DSP block usage by mode; a multiplier that was expected to use a DSP block but appears as logic, or one that consumes a whole block for a narrow multiply, tells you the coding style or widths did not match a supported mode.
