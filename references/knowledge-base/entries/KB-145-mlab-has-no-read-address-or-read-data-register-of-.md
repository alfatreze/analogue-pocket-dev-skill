---
id: KB-145
title: MLAB has no read-address or read-data register of its own; only data-in and output registers exist, which shapes how a registered read is inferred
status: docs-verified
confidence: medium
first_seen: 2026-10-13
last_verified: 2026-10-13
tags: [mlab,inference,registered-read,cyclone-v]
applies_to: Cyclone V E (5CEBA4F23C8, the Analogue Pocket FPGA), Quartus Prime Lite or Standard; Cyclone V Device Handbook Vol 1 as served on docs.altera.com, read 2026-10-13
sources:
  - Cyclone V Device Handbook Volume 1 (docs.altera.com), handbook ch.2: 2.2.1, 2.4 (ROM and shift register rows)
---

## Claim
Because an MLAB is a dual-purpose LAB, only its data input and output registers are inside the block. The read-address register comes from the ALMs around it, while the write-address register and the read-data register are inside the MLAB. The handbook adds that an unregistered address is possible on an MLAB ROM but only in simple dual-port mode. Single-port RAM on an MLAB is emulated by Quartus with minimal extra logic. Practical consequence: an MLAB read that you register in your own code may be mapped onto either the block's output register or ALM registers, and how it lands depends on the exact coding style, which is why small coding differences can flip a memory between MLAB, M10K and plain registers.

## Evidence
Section 2.2.1 states the register layout directly. The inference-style consequence is an engineering inference from that statement and from the project's own fit reports, not a quoted claim.

## How to validate on hardware
Check the Quartus fit report's per-entity RAM table before and after a coding-style change; keep the read as one plain registered read (see the project entries on RAM inference) and confirm the block type did not change.
