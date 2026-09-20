---
id: KB-017
title: Sleep requires savestate support (00A0/00A4)
status: docs-verified
confidence: high
first_seen: 2026-09-20
last_verified: 2026-09-20
tags: [sleep, savestate]
applies_to: all
sources:
  - https://www.analogue.co/developer/docs/core-definition-files/core-json
  - https://github.com/agg23/openfpga-SNES/issues/59
---

## Claim
core.json `sleep_supported` uses host commands 00A0/00A4; a core that cannot create savestates offers only power off. The SNES core stayed without sleep for this reason.

## Evidence
core.json docs and the SNES issue thread.

## How to validate on hardware
Set sleep_supported true only after savestate start/load round-trips on hardware.
