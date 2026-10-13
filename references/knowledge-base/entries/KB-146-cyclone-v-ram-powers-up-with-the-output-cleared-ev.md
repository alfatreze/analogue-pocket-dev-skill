---
id: KB-146
title: Cyclone V RAM powers up with the output cleared even when initialised from a .mif, and MLAB unregistered outputs show contents
status: docs-verified
confidence: high
first_seen: 2026-10-13
last_verified: 2026-10-13
tags: [memory,power-up,initialisation,mif]
applies_to: Cyclone V E (5CEBA4F23C8, the Analogue Pocket FPGA), Quartus Prime Lite or Standard; Cyclone V Device Handbook Vol 1 as served on docs.altera.com, read 2026-10-13
sources:
  - Cyclone V Device Handbook Volume 1 (docs.altera.com), handbook ch.2: 2.2.4 (Table 4)
---

## Claim
All memory blocks accept a .mif, but even a pre-initialised memory powers up with its output cleared. M10K outputs are cleared at power-up whether or not the output register is used. MLAB outputs are cleared only if the output register is used; with the register bypassed, an MLAB reads its contents immediately. Cells that you do not initialise start at zero.

## Evidence
Table 4 (initial power-up values of embedded memory blocks) and the text under it in the handbook.

## How to validate on hardware
If logic evaluates a RAM output right after configuration, simulate with the output forced to zero for the first cycle on M10K, and decide explicitly whether the design depends on the unregistered-MLAB behaviour.
