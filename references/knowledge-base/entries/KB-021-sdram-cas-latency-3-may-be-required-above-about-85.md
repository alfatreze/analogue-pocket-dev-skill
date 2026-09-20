---
id: KB-021
title: SDRAM CAS latency 3 may be required above about 85 MHz
status: community-reported
confidence: low
first_seen: 2026-09-20
last_verified: 2026-09-20
tags: [sdram, timing]
applies_to: UNVERIFIED: taken from a search-result summary; primary source not opened
sources:
  - https://github.com/agg23/analogue-pocket-utils
---

## Claim
A search summary of core repos stated that developers adopted agg23's SDRAM controller clocking and moved to CAS3 because the datasheet recommends CAS3 beyond 85 MHz. Treat as a lead only.

## Evidence
No primary text was read. Open the controller source and the AS4C32M16MSA datasheet before relying on this.


## How to validate on hardware
Read the CAS latency parameter in the SDRAM controller in use and in the mode-register init; test at the configured dram_clk with CAS2 and CAS3 and record errors.
