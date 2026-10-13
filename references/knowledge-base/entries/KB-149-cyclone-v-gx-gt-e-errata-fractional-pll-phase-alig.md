---
id: KB-149
title: Cyclone V GX/GT/E errata: fractional PLL phase alignment error affects inter-clock domain transfers and phase compensation on early die revisions
status: docs-verified
confidence: medium
first_seen: 2026-10-13
last_verified: 2026-10-13
tags: [errata,fractional-pll,clock-domain-crossing,cyclone-v]
applies_to: Cyclone V E (5CEBA4F23C8, the Analogue Pocket FPGA), Quartus Prime Lite or Standard; Cyclone V Device Handbook Vol 1 as served on docs.altera.com, read 2026-10-13
sources:
  - Cyclone V Device Handbook Volume 1 (docs.altera.com), errata document 1.5 and 1.2
---

## Claim
The errata list a fractional-PLL static-phase error that can exceed the Quartus model. It can matter when a fractional PLL is used for phase compensation, for specific IP that requires an fPLL, and for transfers between clock domains that involve an fPLL; frequency range and jitter still meet the datasheet. It is a time-zero condition: a device either shows it from the start or never does. Mitigation is to avoid or harden the clock-domain transfers involved. The errata table names fixed die revisions per device (for example 5CEA4 revision B and 5CEA7 revision C); the Pocket part is a 5CEBA4, which the table does not list by that exact name, so whether it is affected is not established here. A separate erratum notes that JTAG configuration fails if the TCK is clocked through a PAUSE_DR state mid-bitstream (halt TCK instead); there is no planned fix.

## Evidence
Errata sections 1.5 (fractional PLL phase alignment) and 1.2 (JTAG programming of 28 nm devices) in the Cyclone V GX, GT and E errata document on docs.altera.com. Not hardware-tested by this project.

## How to validate on hardware
Treat any dual-clock handoff from an fPLL output as needing a proper synchroniser or FIFO rather than relying on phase; if an intermittent crossing error appears on one unit but not another, suspect this class before the design.
