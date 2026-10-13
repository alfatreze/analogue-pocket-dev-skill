---
id: KB-152
title: 3.3 V LVTTL and 3.3 V LVCMOS have different output guarantees, and the stated levels only hold at the matching current-strength setting
status: docs-verified
confidence: medium
first_seen: 2026-10-13
last_verified: 2026-10-13
tags: [io,lvttl,lvcmos,drive-strength,cyclone-v]
applies_to: Cyclone V E (5CEBA4F23C8, the Analogue Pocket FPGA), Quartus Prime Lite or Standard; Cyclone V Device Handbook Vol 1 as served on docs.altera.com, read 2026-10-13
sources:
  - Cyclone V Device Handbook Volume 1 (docs.altera.com), datasheet I/O specifications (single-ended DC table and its footnote 18); handbook 5.8.1
---

## Claim
Datasheet DC levels at VCCIO 3.135 to 3.465 V: both 3.3 V LVTTL and 3.3 V LVCMOS have VIL max 0.8 V, VIH min 1.7 V and VIH max 3.6 V. Output guarantees differ: 3.3 V LVTTL is VOL max 0.45 V and VOH min 2.4 V at 4 mA; 3.3 V LVCMOS is VOL max 0.2 V and VOH min VCCIO minus 0.2 V at 2 mA. A footnote states that to meet these IOL/IOH numbers the current-strength assignment must be set to that value, because a lower strength may not meet them. Programmable current strength for 3.3 V LVTTL offers 16, 8 and 4 mA (the 3.3 V LVCMOS row lists 2 mA); the handbook advises IBIS or SPICE simulation to choose the strength for a real board.

## Evidence
Datasheet single-ended I/O DC table and footnote 18; handbook Table 50. The default strength in each row is shown in bold in the original, which is not preserved in the text copy used here, so the default is not recorded.

## How to validate on hardware
Read the I/O standard and current strength Quartus reports per pin (fit report, I/O assignment listing) and compare with the receiving device's VIH/VIL at that strength; do not assume the default meets a particular device's thresholds.
