---
id: KB-011
title: Fit results vary about 1.2 ns by seed; re-seed 3-4 times, do not grind, read fast-corner hold
status: community-reported
confidence: high
first_seen: 2026-09-20
last_verified: 2026-09-20
tags: [timing, quartus, seed]
applies_to: Cyclone V 5CEBA4F23C8 at high utilization; two independent projects agree
sources:
  - https://github.com/thekoalakoa/paprium-pocket/blob/master/docs/BUILD_REFERENCE.md
  - https://github.com/janisc/openfpga-NGPC
---

## Claim
At 90-99 percent occupancy placement dominates timing: identical RTL gave 1.19 ns setup spread across four seeds, and hold can fail in the FAST corner while passing slow. One failing fit is not proof a change broke timing. A bitstream with slack near -2.96 ns produced boot garbage while -2.6 booted, so negative slack is not automatically fatal but is not free. Three or four seeds are data; ten is a lottery.

## Evidence
Paprium's measured sweep table and NGPC's 'fit battles and seed sweeps' statement.

## How to validate on hardware
Run 4 seeds of the same RTL and record setup, hold (both corners) and TNS; check whether the observed hardware fault tracks slack.
