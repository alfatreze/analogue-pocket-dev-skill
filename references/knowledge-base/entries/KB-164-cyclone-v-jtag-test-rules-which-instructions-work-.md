---
id: KB-164
title: Cyclone V JTAG test rules: which instructions work during configuration, which pins and rail it uses, and how it can only be disabled with pin ties
status: docs-verified
confidence: medium
first_seen: 2026-10-13
last_verified: 2026-10-13
tags: [jtag,boundary-scan,configuration,pins,cyclone-v]
applies_to: Cyclone V E (5CEBA4F23C8, the Analogue Pocket FPGA), Quartus Prime Lite or Standard; Cyclone V Device Handbook Vol 1 as served on docs.altera.com, read 2026-10-13
sources:
  - Cyclone V Device Handbook Volume 1 (docs.altera.com), handbook ch.9: 9.2 to 9.5
---

## Claim
BYPASS, IDCODE and SAMPLE can be issued before, after or during configuration without interrupting it. Other instructions need nCONFIG held low (before configuration) or CONFIG_IO to interrupt configuration (during it); PULSE_NCONFIG or an nCONFIG pulse then reconfigures. EXTEST is not supported during in-circuit reconfiguration, and after configuration differential pin pairs cannot be tested. A SAMPLE/PRELOAD cycle should precede the first EXTEST so known data sits at the pins. The chip-wide reset DEV_CLRn and output enable DEV_OE do not disturb boundary-scan or configuration. The four JTAG pins (TDI, TDO, TMS, TCK) are powered by the VCCPD supply of bank 3A (2.5, 3.0 or 3.3 V); TRST is not supported; TCK has an internal weak pull-down and TDI and TMS weak pull-ups; all user I/O are tri-stated during JTAG configuration. If the 10 pattern does not shift out on the first SHIFT_IR clock, the TAP is not in the right state (go to reset and send the TMS sequence 01100) or the power, ground or configuration pins are wrong. JTAG cannot be turned off in software: tie TMS and TDI to the bank 3A VCCPD supply, TCK to ground and leave TDO open.

## Evidence
Sections 9.2 to 9.5 and Table 115 of the handbook.

## How to validate on hardware
When a chain scan fails, check bank 3A VCCPD, the pull-ups on TMS/TDI and the configuration pins before suspecting the cable; when scripting, issue CONFIG_IO only after nSTATUS is high.
