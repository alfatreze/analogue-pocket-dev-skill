---
id: KB-005
title: Target data-slot write (0184) reliability is disputed
status: disputed
confidence: low
first_seen: 2026-09-20
last_verified: 2026-09-20
tags: [target-commands, save, firmware]
applies_to: conflicting claims across firmware eras
sources:
  - https://github.com/agg23/openfpga-litex/blob/main/docs/control.md
  - https://github.com/open-fpga/core-example-kbmouse-targetdata
  - https://www.analogue.co/developer/docs/changelog/1-1-beta-7
---

## Claim
LiteX docs say SD write via target commands 'appears to be broken in the Pocket firmware' and recommend avoiding it. Analogue's kbmouse example README claims Select saves the framebuffer to slot 0x22 via target write. The 1.1 beta 7 changelog lists 'Fixed truncation bug in Target command [0184]'.

## Evidence
The LiteX note is undated and likely predates later fixes; the official example shipped as working. No source here reproduces a failure on current firmware.

## How to validate on hardware
Run the kbmouse example on the current firmware and confirm `saved.bin` is created with the expected size and contents. Note firmware version.
