---
id: KB-160
title: Cyclone V hot-socketing keeps outputs tri-stated and pulled up during power-up and configuration, except nSTATUS and CONF_DONE
status: docs-verified
confidence: medium
first_seen: 2026-10-13
last_verified: 2026-10-13
tags: [power,hot-socketing,io,configuration,cyclone-v]
applies_to: Cyclone V E (5CEBA4F23C8, the Analogue Pocket FPGA), Quartus Prime Lite or Standard; Cyclone V Device Handbook Vol 1 as served on docs.altera.com, read 2026-10-13
sources:
  - Cyclone V Device Handbook Volume 1 (docs.altera.com), handbook ch.10: 10.2, 10.3
---

## Claim
Hot-socketing circuitry watches VCCIO, VCCPD and VCC and allows the supplies in any order. Signals may be driven into I/O, dedicated input and dedicated clock pins before or during power-up or power-down without damage, input signals cannot back-feed the supplies, the output buffers are tri-stated until user mode, and the device is immune to latch-up when inserted into a live board. Pin capacitance during hot-socketing is under 15 pF for I/O and under 20 pF for clock pins. The weak pull-up in each I/O element is on during configuration so pins do not float. The configuration pins nSTATUS and CONF_DONE are exempt and do drive during power-up and power-down so configuration can run. The handbook asks that board ground be connected before the supplies.

## Evidence
Sections 10.2 and 10.3 of the handbook.

## How to validate on hardware
Check that no external device treats a weak-pull-up level on an FPGA pin as valid data during configuration, and that nothing relies on the FPGA actively driving a line before user mode.
