---
id: KB-165
title: The 5CEBA4 has 18,480 ALMs with four registers each in LABs of ten, and each LAB has only two clock sources and three clock enables
status: docs-verified
confidence: medium
first_seen: 2026-10-13
last_verified: 2026-10-13
tags: [alm,lab,logic,registers,clocking,cyclone-v]
applies_to: Cyclone V E (5CEBA4F23C8, the Analogue Pocket FPGA), Quartus Prime Lite or Standard; Cyclone V Device Handbook Vol 1 as served on docs.altera.com, read 2026-10-13
sources:
  - Cyclone V Device Handbook Volume 1 (docs.altera.com), handbook ch.1: 1.1; device overview resource table
---

## Claim
The Cyclone V E A4 lists 18,480 ALMs (49 K logic elements) and 73,920 registers, i.e. four programmable registers per ALM. Ten ALMs form a LAB, and up to a quarter of the LABs can act as MLABs (640-bit simple dual-port memory, 32 x 2 per ALM). Each register has data, clock, synchronous and asynchronous clear and synchronous load ports; clock and clear can come from global signals, pins or logic, while the clock enable comes from pins or logic. A LAB has dedicated control logic offering two clock sources and three clock enables (an inverted clock counts as a separate source), and a clock enable switches off its linked LAB-wide clock. A LAB drives 30 ALMs through fast local and direct-link interconnect (its own ten plus those of each adjacent LAB), and neighbouring LABs, MLABs, M10K and DSP blocks can drive its local interconnect directly. Register packing lets unrelated registers and combinational logic share an ALM, and a register can feed back into the LUT in the same ALM. An engineering inference, not a handbook statement: because the per-LAB control signals are so few, a design with many distinct clocks, enables or resets spread across small groups of registers packs less densely than one with a few shared controls.

## Evidence
Section 1.1 (1.1.1 to 1.1.5) of the handbook and the A4 column of the resource table in the Device Overview (18,480 ALMs, 73,920 registers). The packing-density inference is the author's reading of the LAB control limits, not a measured result.

## How to validate on hardware
In the Quartus fit report compare the ALM count with the register count (a ratio well below four registers per ALM at high utilisation points to control-signal or routing limits), and check how many distinct enable and reset nets a heavily used block has.
