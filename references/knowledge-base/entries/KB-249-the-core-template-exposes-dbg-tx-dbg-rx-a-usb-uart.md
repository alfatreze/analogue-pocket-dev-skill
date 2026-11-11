---
id: KB-249
title: The core template exposes dbg_tx/dbg_rx (a USB UART to a breakout board) and user1/user2 (pads near the JTAG connector a user can solder to), tied off by default
status: community-reported
confidence: low
first_seen: 2026-11-11
last_verified: 2026-11-11
tags: [uart,debug,pads,template,hardware]
applies_to: Analogue core template (open-fpga/core-template core_top.template.v); not tested on hardware
sources:
  - https://github.com/open-fpga/core-template
---

## Claim
The template top level declares dbg_tx (output) and dbg_rx (input) under the comment 'i/o to 6515D breakout usb uart', and user1 (output) and user2 (input) under 'i/o pads near jtag connector user can solder to'. The template ties dbg_tx and user1 to high impedance. The template also lists aux_sda/aux_scl as an internal I2C bus marked 'RFU, do not use'. So the template points at two serial paths that need no link cable and no cartridge power: a USB UART on a breakout board (probably the developer key hardware, not confirmed) and two solder pads by the JTAG connector. Their voltage, pad locations and whether retail units route them are not documented in the pages read.

## Evidence
Source read: repo-src/core_top.template.v lines 132-147 and 305-307 (Analogue's template, one source). No documentation page found that explains the pads or the breakout. Not hardware-verified.

## How to validate on hardware
On a unit with the JTAG header exposed, find the two pads near it (continuity to the FPGA pin names from the template, or the board photos in Analogue's developer material). Drive user1 with a slow square wave from a core and measure it with a scope; measure the voltage level before connecting any adapter.
