---
id: KB-258
title: A CPU MMIO register decode that ignores upper address bits aliases new registers placed above the page onto old ones: a 9-bit decode maps 0x280 onto 0x080
status: community-reported
confidence: low
first_seen: 2026-11-26
last_verified: 2026-11-26
tags: [mmio,address-decode,soft-cpu]
applies_to: any soft-CPU core with a register page decoded from a fixed number of low address bits; observed in one core under test
evidence: first-hand: read the RTL decode and the register allocation table of one core under test, 2026-11-25; not run on hardware
sources:
  - first-hand: RTL and register map of one core under test, read 2026-11-25 (no vendor document was read for this claim)
---

## Claim

If the CPU's MMIO peripheral decodes only the low N bits of the register offset, a register placed at or above 2^N is not a new register: it aliases onto the offset formed by the low N bits and so reads and writes whatever lives there. In one core a 9-bit decode (a 512-byte page) maps a proposed register at 0x280 onto 0x080, which already holds other registers. Adding registers above the page therefore needs a wider decode (and any register mirror in tools or tests updated), not just a new address.

## Evidence

First-hand, one core under test, 2026-11-25: while allocating a block of five registers at 0x280 to 0x290 for a second display mode, the allocation table showed only 0x1F8 to 0x1FC free in the 9-bit page and the decode used the low nine bits, so 0x280 landed on an existing register group. Found by reading RTL and the table; no hardware test was run.

## How to validate on hardware

Write a distinct value to a register above the page and read back the register at the aliased offset; or in simulation, access both offsets and compare. Widen the decode and repeat.
