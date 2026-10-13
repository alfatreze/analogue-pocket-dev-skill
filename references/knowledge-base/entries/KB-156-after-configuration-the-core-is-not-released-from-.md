---
id: KB-156
title: After configuration the core is not released from reset all at once: hold the design in reset for 175 to 437 microseconds and let external devices ignore the FPGA until INIT_DONE
status: docs-verified
confidence: medium
first_seen: 2026-10-13
last_verified: 2026-10-13
tags: [configuration,reset,user-mode,init-done,cyclone-v]
applies_to: Cyclone V E (5CEBA4F23C8, the Analogue Pocket FPGA), Quartus Prime Lite or Standard; Cyclone V Device Handbook Vol 1 as served on docs.altera.com, read 2026-10-13
sources:
  - Cyclone V Device Handbook Volume 1 (docs.altera.com), handbook ch.7: 7.3.1 to 7.3.6; datasheet configuration timing (tCD2UM)
---

## Claim
Until the device is configured every user I/O is tied to a weak internal pull-up. After CONF_DONE goes high the device initialises (default clock: the internal oscillator, or CLKUSR/DCLK if chosen) and enters user mode; registers, core logic and I/O are not all released from reset at the same moment, and the handbook says larger and faster designs need a reset strategy for that. Its recommendation: hold the whole design in reset for the CONF_DONE-to-user-mode interval before doing anything (datasheet tCD2UM is 175 to 437 microseconds; with CLKUSR it is tCD2CU plus Tinit clock periods). An external device that reacts to an FPGA output should ignore that pin, or have its input held constant, until the optional INIT_DONE pin goes high. A reconfiguration is started by pulling nCONFIG low for at least tCFG, which also pulls nSTATUS and CONF_DONE low and returns the I/O to weak pull-ups. Error handling is either the Auto-restart option or watching nSTATUS.

## Evidence
Sections 7.3.1 to 7.3.6 of the handbook and the datasheet configuration-timing table (tCD2UM row). Which of these pins the Analogue Pocket exposes to a core is not covered here; the Pocket's own system side drives configuration.

## How to validate on hardware
In simulation or on a bench, generate the core's reset from a counter that starts at user mode and lasts longer than 437 microseconds of the slowest clock, and verify every state machine is idle until it expires.
