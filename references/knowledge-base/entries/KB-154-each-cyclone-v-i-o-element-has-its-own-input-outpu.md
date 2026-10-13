---
id: KB-154
title: Each Cyclone V I/O element has its own input, output and output-enable registers; that is what makes pin registers 'fast' and ties pin timing to register packing
status: docs-verified
confidence: medium
first_seen: 2026-10-13
last_verified: 2026-10-13
tags: [io,ioe,registers,packing,timing,cyclone-v]
applies_to: Cyclone V E (5CEBA4F23C8, the Analogue Pocket FPGA), Quartus Prime Lite or Standard; Cyclone V Device Handbook Vol 1 as served on docs.altera.com, read 2026-10-13
sources:
  - Cyclone V Device Handbook Volume 1 (docs.altera.com), handbook ch.5: 5.7
---

## Claim
The I/O element (IOE) contains a bidirectional buffer plus registers for the input path (pin to core), the output path (core to pin) and the output-enable path, with optional DDR registers, alignment and synchronisation registers, and half-rate blocks. Each block in these paths can be bypassed, and the input path includes a deskew delay that tracks process, voltage and temperature. The IOE registers allow faster source-synchronous register-to-register transfers and resynchronisation. This is the hardware that a design uses when Quartus packs a register into an I/O cell; if the register has more than the single load the I/O cell allows, or a conflicting clear/load structure, it stays in the fabric (Quartus packs a register into the I/O cell only when that register has a single load and no conflicting clear/load structure).

## Evidence
Section 5.7 and Table 48 and Figure 81 of the handbook. The packing conditions in the claim come from observed Quartus behaviour, not from this chapter.

## How to validate on hardware
In the fit report look at the I/O register packing summary for each pin; an output-data or output-enable register that was not packed explains extra clock-to-output time compared with the figure the datasheet quotes for a packed register.
