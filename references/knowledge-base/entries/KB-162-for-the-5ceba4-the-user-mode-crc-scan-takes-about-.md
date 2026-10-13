---
id: KB-162
title: For the 5CEBA4 the user-mode CRC scan takes about 9 ms to 2.76 s per full pass, set by a 2^n divider on a 100 MHz internal oscillator
status: docs-verified
confidence: medium
first_seen: 2026-10-13
last_verified: 2026-10-13
tags: [seu,crc,error-detection,timing,cyclone-v]
applies_to: Cyclone V E (5CEBA4F23C8, the Analogue Pocket FPGA), Quartus Prime Lite or Standard; Cyclone V Device Handbook Vol 1 as served on docs.altera.com, read 2026-10-13
sources:
  - Cyclone V Device Handbook Volume 1 (docs.altera.com), handbook ch.8: 8.5 (Tables 104 to 106)
---

## Claim
The error-detection clock comes from the internal oscillator (42.6 to 100 MHz depending on the device) divided by 2^n with n from 0 to 8, so the scan frequency runs from 100 MHz down to about 390 kHz. For the Cyclone V E A4 member: the estimated minimum interval between updates of the error message register is 1.47 microseconds; the time to run the CRC over the whole device is tMIN 9 ms (fastest clock, minimum divider setting 2) up to tMAX 2.76 s (slowest clock, n = 8). The formulas given scale tMAX by 2^(n-8) and tMIN by 2^n over the minimum divider. A slower scan lowers power and raises the time to notice and recover from a soft error.

## Evidence
Tables 104, 105 and 106 and the formulas in 8.5.1 to 8.5.3 of the handbook.

## How to validate on hardware
If a design enables CRC detection, record the divider setting and compute the worst-case time to notice an upset from the formulas; compare with the system's tolerance for an undetected flipped configuration bit.
