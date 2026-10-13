---
id: KB-144
title: Read-during-write behaviour is block-specific: M10K cannot return new data on a mixed-port read, MLAB can only do it with a registered output
status: docs-verified
confidence: high
first_seen: 2026-10-13
last_verified: 2026-10-13
tags: [memory,read-during-write,m10k,mlab,inference]
applies_to: Cyclone V E (5CEBA4F23C8, the Analogue Pocket FPGA), Quartus Prime Lite or Standard; Cyclone V Device Handbook Vol 1 as served on docs.altera.com, read 2026-10-13
sources:
  - Cyclone V Device Handbook Volume 1 (docs.altera.com), handbook ch.2: 2.2.3 (Tables 2 and 3)
---

## Claim
Same-port read-during-write (single-port RAM or one port of a true dual-port RAM): M10K offers "new data" (flow-through) or "don't care"; MLAB offers only "don't care". Mixed-port read-during-write (one port reads the address another port writes, same clock): M10K offers "old data" or "don't care"; MLAB offers "old data", "new data" (registered output only), "don't care" and "constrained don't care". For M10K "don't care" Quartus does not analyse write-to-read timing; for MLAB it does by default (the setting that disables this assumes you never read and write the same address in the same cycle). Memory blocks have no internal conflict resolution when two ports write the same address in true dual-port mode.

## Evidence
Tables 2 and 3 and the surrounding text in the handbook. Consistent with the project observation that an M10K cannot give a same-cycle forwarded value on a mixed-port read, which is why designs that need it build explicit bypass logic or accept one cycle of latency.

## How to validate on hardware
If simulation assumes a read sees a same-cycle write, check which of the four modes the inferred RAM really uses (the RAM IP cores show the choice; inferred RAM follows the coding style). A functional mismatch between simulation and hardware at the write address is the signature.
