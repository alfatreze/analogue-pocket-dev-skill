---
id: KB-163
title: The Cyclone V E A4 JTAG IDCODE is 0x02B050DD, and the instruction codes SAMPLE/PRELOAD, IDCODE, BYPASS and CONFIG_IO are fixed by the handbook
status: docs-verified
confidence: high
first_seen: 2026-10-13
last_verified: 2026-10-13
tags: [jtag,idcode,boundary-scan,signaltap,cyclone-v]
applies_to: Cyclone V E (5CEBA4F23C8, the Analogue Pocket FPGA), Quartus Prime Lite or Standard; Cyclone V Device Handbook Vol 1 as served on docs.altera.com, read 2026-10-13
sources:
  - Cyclone V Device Handbook Volume 1 (docs.altera.com), handbook ch.9: 9.1 (Tables 112 and 113)
---

## Claim
The IDCODE is 32 bits: a 4-bit version (0), a 16-bit part number, an 11-bit manufacturer identity and a trailing 1. For the Cyclone V E A4 the part number is 0010 1011 0000 0101, giving 0x02B050DD (the A5 is 0x02B220DD, the A2 0x02B150DD, the SE/SX A4 or C4 0x02D010DD). Ten-bit instruction codes: SAMPLE/PRELOAD 0x005 (also used by the SignalTap logic analyser), EXTEST 0x00F, BYPASS 0x3FF, USERCODE 0x007, IDCODE 0x006 (the default instruction at power-up and in the TAP reset state), HIGHZ 0x00B, CLAMP 0x00A, PULSE_NCONFIG 0x001, CONFIG_IO 0x00D (only after nSTATUS goes high), LOCK 0x1F0 and UNLOCK 0x331 (secure mode, reachable only through JTAG core access in user mode). The handbook notes that after configuration the weak pull-up or bus-hold features override HIGHZ and CLAMP values at the pin.

## Evidence
Tables 112 and 113 of the handbook. A USB-Blaster chain scan of a Pocket's FPGA reports this A4 IDCODE (a developer's JTAG session, not part of the handbook), which independently fits an E-series A4.

## How to validate on hardware
Run a JTAG chain scan (jtagconfig or equivalent) and compare the reported IDCODE with the value above; a different part number means a different device variant.
