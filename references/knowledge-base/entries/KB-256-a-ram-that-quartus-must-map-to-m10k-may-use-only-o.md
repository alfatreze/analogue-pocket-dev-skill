---
id: KB-256
title: A RAM that Quartus must map to M10K may use only one address per port: a separate write address and read address on the same port fail synthesis
status: community-reported
confidence: low
first_seen: 2026-11-23
last_verified: 2026-11-23
tags: [quartus,m10k,ram,synthesis]
applies_to: Quartus Prime Lite (version as in the fit manifest of the core under test), Cyclone V 5CEBA4F23C8; one observation
evidence: first-hand synthesis failure and fix in one core under test, 2026-11-22
sources:
  - first-hand: a Quartus Prime Lite fit of a Cyclone V core under test, 2026-11-22 (no vendor document was read for this claim)
---

## Claim

A dual-port RAM described in HDL maps to M10K blocks only if each port has ONE address. A port that writes at one address (for example the bridge's write index) and reads at another (a separately latched read index) in the same clocked block is not a legal M10K port: Analysis & Synthesis fails with `Error (10028): Can't resolve multiple constant drivers for net "mem[0][31]"` and `Error (12152): Can't elaborate user hierarchy` (the array falls back to registers, and an `initial` loop becomes a second driver). Fix: one address expression per port, for example `addr = we ? write_idx : read_idx`, valid when a write and a read never overlap in time. Host simulation (Icarus) cannot see this: it runs the design as written. After launching a fit of a changed memory, confirm Analysis & Synthesis succeeded (about 5 minutes) before leaving it.

## Evidence

First-hand, one core under test, 2026-11-22: a fit failed at the 5-minute synthesis mark with the two errors above after a change gave the bridge port a latched read address next to its write address; the same RAM with one address per port (`a_we ? a_idx : r_idx`) synthesised, fitted (RAM blocks 281 of 308) and ran on a Pocket. No vendor text was read for this claim, so confidence is low; it matches the general rule that an M10K port has a single address bus.

## How to validate on hardware

Not a hardware question: run Analysis & Synthesis on a small module with a port that uses two addresses in one `always` block and read the messages, then merge the addresses into one expression and re-run; check the fit report's RAM block count.
