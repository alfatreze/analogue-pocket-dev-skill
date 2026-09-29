---
id: KB-076
title: Fence bridge-written slot data at dataslot_allcomplete, or run the save RAM in the bridge clock domain, so no write is still crossing the CDC when the core starts
status: community-reported
confidence: low
first_seen: 2026-09-29
last_verified: 2026-09-29
tags: [bridge,cdc,loader,psram,save]
applies_to: two community cores (a GBA port v0.8.0, 2026-09-27; a Doom port v1.2.0, 2026-04-01); Cyclone V Pocket, PSRAM-backed saves
sources:
  - https://github.com/mincer-ray/openfpga-GBA
  - https://github.com/thinkelastic/PocketDoom/releases/tag/v1.2.0
---

## Claim

Slot data written over the bridge (clk_74a) usually crosses into the core's memory clock through a FIFO.
The APF's "all slots complete" signal arrives in the bridge domain and can overtake writes still queued
in that FIFO, or still pending at the memory. Two cores solve this in different ways:

- **Ordered fence (GBA port, `apf_write_ingress.sv`):** each whole 32-bit bridge write goes into one CDC
  FIFO. On the rising edge of `dataslot_allcomplete` a fence token is queued behind the data. The core is
  released only after the fence has passed every earlier write, including the physical PSRAM write.
  Per-slot consumers (an RTC sidecar parser in that core) validate what they received only after the fence.
- **No crossing (Doom port):** "PSRAM1 reclocked to bridge domain (74.25 MHz) — Eliminates all CDC FIFOs for
  save data. Bridge writes directly to PSRAM with zero data loss."

The Doom release notes also mention "4-byte sacrificial padding — absorbs PSRAM first-byte corruption during
burst-mode transitions". That is an unexplained workaround in one core. Treat it as a lead only.

The GBA port also moved an RTC timestamp out of the save file into its own 16-byte nonvolatile slot
(`size_exact 16`, a separate bridge address). The `.sav` then keeps the standard size and works in other
emulators.

## Evidence

GBA port: source read (the new `apf_write_ingress.sv` header says "A fence is inserted after
dataslot_allcomplete and is released only after every earlier halfword and physical PSRAM write has
completed"), plus the data.json diff adding slot id 11. Doom port: release notes only; the RTL was not
read. No write-up describes a failure that the fence fixed, so the problem it guards against is inferred
from the design.

## How to validate on hardware

In simulation, drive a burst of bridge writes and assert `dataslot_allcomplete` on the last one. Then
check whether the core leaves reset before the last word reaches memory. On hardware, load a slot whose
last bytes are distinctive (a checksum or a magic value at the very end) and verify it before starting
the core. Repeat many boots with the largest slot the core accepts.
