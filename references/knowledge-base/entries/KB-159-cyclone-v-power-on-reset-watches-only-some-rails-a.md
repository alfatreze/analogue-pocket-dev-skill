---
id: KB-159
title: Cyclone V power-on reset watches only some rails and tri-states all I/O if the supplies do not ramp within tRAMP; VCCPD must be at least VCCIO
status: docs-verified
confidence: medium
first_seen: 2026-10-13
last_verified: 2026-10-13
tags: [power,por,vccpd,vccio,ramp,cyclone-v]
applies_to: Cyclone V E (5CEBA4F23C8, the Analogue Pocket FPGA), Quartus Prime Lite or Standard; Cyclone V Device Handbook Vol 1 as served on docs.altera.com, read 2026-10-13
sources:
  - Cyclone V Device Handbook Volume 1 (docs.altera.com), handbook ch.10: 10.4, 10.5; ch.7: 7.3.1; datasheet POR table
---

## Claim
The POR circuit holds the device in reset until all monitored supplies reach their operating range within the maximum ramp time tRAMP; if that is missed the I/O pins and programming registers stay tri-stated and configuration can fail (hold nCONFIG low until the rails are good). Monitored rails: VCC, VCC_AUX, VCCBAT, VCCPD, VCCPGM (plus HPS rails on SoC parts). Not monitored: VCCIO, VCCA_FPLL and the transceiver rails. VCCBAT must be powered for the device to exit POR even when no volatile key is used. VCCPD (2.5, 3.0 or 3.3 V) powers the I/O pre-drivers and JTAG pins: it must be 2.5 V when a bank's VCCIO is 2.5 V or lower, and at least VCCIO above that (3.3 V when VCCIO is 3.3 V). The POR delay set by the MSEL pins is 4 to 1274 ms for the fast option and 100 to 300 ms for the standard option (datasheet). The recommended power-up sequence brings Group 1 rails to at least 80 percent before Group 2; VCCBAT can come up at any time.

## Evidence
Sections 10.4 and 10.5 (Table 118), 7.3.1 and the POR delay table of the datasheet. A board's actual sequencing is set by its power-management design, which this document cannot tell.

## How to validate on hardware
On a bench, capture the supply rails and nSTATUS together at power-up and check that every monitored rail meets tRAMP and that VCCPD is never below VCCIO for a 3.3 V bank.
