---
id: KB-259
title: VexRiscv_Full instruction and data caches are 4 KiB direct-mapped with 32-byte lines: link order alone moves instruction-cache misses by about 3 percent of cycles
status: community-reported
confidence: low
first_seen: 2026-11-26
last_verified: 2026-11-26
tags: [vexriscv,cache,performance,riscv]
applies_to: the generated VexRiscv_Full.v of one core under test (RV32IM, no FPU); the numbers are from a host cache model, not a hardware counter
evidence: first-hand: read the generated RTL configuration; host RV32IM profile with a cache model of 13 link orders of one decoder, 2026-11-25
sources:
  - first-hand: generated VexRiscv_Full.v of one core under test; a host instruction-set profiler with a cache model, 2026-11-25 (no vendor document was read for this claim)
---

## Claim

In the generated VexRiscv used by one core, both caches are 4 KiB, direct-mapped, 32-byte lines (128 lines). With a cache that small, where hot code and hot data sit in the address space matters: two hot loops or arrays that map to the same cache sets evict each other on every pass. A host profile that models the caches (write-through, no write-allocate, about 12 cycles per miss) lands much closer to hardware timing than one without: the hardware-over-model cycle ratio was about 1.34 to 1.38 without the cache model and about 1.15 to 1.19 with it (hardware figures quoted from earlier measurements, not re-measured here).

## Evidence

First-hand, 2026-11-25: 13 link orders of the same decoder code produced 1,450 to 2,411 instruction-cache misses per audio frame (about 3 percent of the cycles); a synthetic loop whose scratch buffer aliased its output array missed 2.4 times more per granule than the same loop with disjoint sets (567 against 236), and two code blocks forced onto the same sets missed 268,009 times against 16,071 on disjoint sets. The cache geometry was read from the generated RTL. These are model results for one decoder; no hardware cache counter was read.

## How to validate on hardware

Read a cache-miss or cycle counter around the hot loop on the device, change the link order or scratch placement, and compare; or add the geometry above to an instruction-set simulator and check that its cycle counts approach the hardware ones.
