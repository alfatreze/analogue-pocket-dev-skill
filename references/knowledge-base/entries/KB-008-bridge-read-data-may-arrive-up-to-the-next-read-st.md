---
id: KB-008
title: Bridge read data may arrive up to the next read strobe
status: hardware-validated
confidence: high
first_seen: 2026-09-20
last_verified: 2026-11-23
tags: [bridge, timing, reads]
applies_to: all framework versions
evidence: A core under test on a Pocket (2026-11-22): the shell latches the address, samples bridge_rd_data for the host, then pulses bridge_rd with the address held; the word requested by that strobe is returned by the NEXT transaction (the host discards a first priming return). A core answering for the live address delivered file word j = RAM word j+1 and a zero last word; latching the address at the strobe fixed it.
sources:
  - https://www.analogue.co/developer/docs/bus-communication
---

## Claim
Reads are buffered: on receiving a read the core may not immediately provide data and has until the next read strobe to drive bridge_rd_data. Return paths must tolerate this and not assume single-cycle data.

## Evidence
Bus Communication page, BRIDGE section.


## How to validate on hardware
Testbench with back-to-back bridge reads separated by 1 cycle and by many cycles; check no value is delivered one beat late or stale.
