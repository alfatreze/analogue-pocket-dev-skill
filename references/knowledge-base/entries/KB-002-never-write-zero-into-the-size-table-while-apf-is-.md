---
id: KB-002
title: Never write zero into the size table while APF is still delivering slots
status: community-reported
confidence: medium
first_seen: 2026-09-20
last_verified: 2026-09-20
tags: [save, size-table, boot]
applies_to: observed on hardware by one project (NGPC)
sources:
  - https://github.com/janisc/openfpga-NGPC/blob/main/target/pocket/core_top.v
---

## Claim
APF uses the same size-table BRAM as its own bookkeeping while delivering data slots. Writing 0 to a slot's entry during delivery made APF deliver exactly one 512-byte sector and stop cleanly.

## Evidence
NGPC core_top comment: the first version stomped the entry to 0 while the save slot streamed in; measured by ingest counters: 256 beats, 0 drops. The NES core writes continuously but its has_save is known from the cartridge header before the save slot streams.

## How to validate on hardware
Write the entry only after `dataslot_allcomplete` (or only when nonzero and known), and compare bytes delivered with and without an early zero write using a beat counter on the bridge write strobe.
