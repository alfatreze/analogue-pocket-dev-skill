---
id: KB-008
title: Bridge read data may arrive up to the next read strobe
status: docs-verified
confidence: high
first_seen: 2026-09-20
last_verified: 2026-09-20
tags: [bridge, timing, reads]
applies_to: all framework versions
sources:
  - https://www.analogue.co/developer/docs/bus-communication
---

## Claim
Reads are buffered: on receiving a read the core may not immediately provide data and has until the next read strobe to drive bridge_rd_data. Return paths must tolerate this and not assume single-cycle data.

## Evidence
Bus Communication page, BRIDGE section.


## How to validate on hardware
Testbench with back-to-back bridge reads separated by 1 cycle and by many cycles; check no value is delivered one beat late or stale.
