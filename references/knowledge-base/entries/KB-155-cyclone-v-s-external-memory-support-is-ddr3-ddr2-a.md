---
id: KB-155
title: Cyclone V's external-memory support is DDR3, DDR2 and LPDDR2; SDR SDRAM and asynchronous PSRAM are ordinary 3.3 V fabric I/O with no hard controller
status: docs-verified
confidence: medium
first_seen: 2026-10-13
last_verified: 2026-10-13
tags: [external-memory,sdram,psram,io,cyclone-v]
applies_to: Cyclone V E (5CEBA4F23C8, the Analogue Pocket FPGA), Quartus Prime Lite or Standard; Cyclone V Device Handbook Vol 1 as served on docs.altera.com, read 2026-10-13
sources:
  - Cyclone V Device Handbook Volume 1 (docs.altera.com), handbook ch.6: 6, 6.1, 6.5; ch.5: 5.1
---

## Claim
The handbook's list of supported external memory standards contains only DDR3 SDRAM, DDR2 SDRAM and LPDDR2 SDRAM, each with a hard memory controller (dedicated pins, up to 8/16/32-bit data, out-of-order command handling, closed-page bank management by default) or a soft controller, with maximum frequencies of 333 to 400 MHz for the hard controller. Neither SDR SDRAM nor asynchronous PSRAM appears, so a core that uses them (as the Pocket core does for its SDRAM and cram PSRAM) implements the controller in fabric logic on regular GPIO pins with the same LVTTL/LVCMOS rules as any other pin. The hard controller's dedicated pins become ordinary I/O when it is not used. The A4 member in the F484 package lists 224 GPIO.

## Evidence
Table 68 (supported standards), Table 69 (performance), 6.5 (hard memory controller) and the package plan Table 26 for the A4 / F484 entry. That the Pocket uses SDR SDRAM and async PSRAM comes from the project, not this document. The package is read from the part number 5CEBA4F23C8 (F23 meaning the 484-pin FineLine BGA), which is an inference from the naming scheme.

## How to validate on hardware
Do not look for a vendor IP or hard-controller recipe for SDR SDRAM or PSRAM on this device; treat the interface as a custom fabric design and verify its read-capture timing and I/O register packing with the Timing Analyzer and a hardware test.
