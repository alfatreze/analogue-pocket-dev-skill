---
id: KB-006
title: Target read/write with length 0xFFFFFFFF was buggy in 1.1 and fixed in 2.1
status: docs-verified
confidence: high
first_seen: 2026-09-20
last_verified: 2026-09-20
tags: [target-commands, changelog]
applies_to: framework 1.1 to 2.0 affected
sources:
  - https://www.analogue.co/developer/docs/changelog/2-1
  - https://github.com/agg23/openfpga-litex/blob/main/docs/control.md
---

## Claim
Length 0xFFFFFFFF (meaning whole file) did not work as documented in framework 1.1 (request the file size instead); 2.1 fixed data slot read/write when length is 0xFFFFFFFF.

## Evidence
2.1 changelog: 'Fixed data slot read/write commands when length is 0xFFFFFFFF'. LiteX notes the 1.1 bug.

## How to validate on hardware
On current firmware read a small deferload slot with length 0xFFFFFFFF and confirm the clamped length.
