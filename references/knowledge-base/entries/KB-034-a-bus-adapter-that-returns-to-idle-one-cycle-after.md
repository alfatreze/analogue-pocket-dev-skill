---
id: KB-034
title: A bus adapter that returns to idle one cycle after ACK re-accepts a completed beat when the CPU-side ACK is registered
status: community-reported
confidence: medium
first_seen: 2026-09-20
last_verified: 2026-09-20
tags: [bus, handshake, design-lesson, cpu]
applies_to: general RTL design lesson; found in one core's CPU-to-memory adapter
sources:
  - Hardware observation and simulation by the skill author, 2026-09-20 (no public artifact)
  - https://www.analogue.co/developer/docs/bus-communication
---

## Claim
If an adapter returns to idle a fixed one cycle after issuing its ACK while the CPU-side ACK is registered once more, the CPU still presents the completed beat during that cycle. The adapter accepts it a second time and sends a duplicate downstream request. The duplicate's completion then acknowledges the NEXT beat with the previous beat's data, so every following transfer lags by one beat while memory contents stay correct. Return to idle only after the master has observed the ACK (two cycles after the ACK in this design).

## Evidence
On hardware, CPU writes landed (verified through a separate mailbox read) but reads that followed another CPU beat returned the previous beat's data. An Icarus regression using the real adapter, mux, bridge and arbiter with a registered-ACK CPU model reproduced it (18 beats produced 19 bridge requests; loads lagged one beat) and passed after adding a second release state. The Pocket then passed a 183-check CPU-window matrix and two further cold-boot runs (user-reported). This is a general design lesson from one bug, not an APF statement; APF's own read contract (bridge data may arrive up to the next read strobe, KB-008) is separate.

## How to validate on hardware
Simulate the exact master handshake (registered ACK, STB held into the next beat) and assert one downstream request per beat and correct data on back-to-back reads and store-then-load, before running on hardware.
