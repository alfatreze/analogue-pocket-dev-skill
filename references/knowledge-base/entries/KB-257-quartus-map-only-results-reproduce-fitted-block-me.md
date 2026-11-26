---
id: KB-257
title: Quartus map-only results reproduce fitted block-memory bits exactly and logic within about 5 percent: use map deltas to rank features, fitted figures to budget
status: community-reported
confidence: low
first_seen: 2026-11-26
last_verified: 2026-11-26
tags: [quartus,resources,estimate,synthesis]
applies_to: Quartus Prime Lite 25.1 (as in the fit manifest of the core under test), Cyclone V 5CEBA4F23C8; one calibration point
evidence: first-hand: ten map-only runs of one graphics-engine entity compared with the fitted figures of the same module from earlier full fits of one core under test, 2026-11-25
sources:
  - first-hand: quartus_map runs on a build VM, 2026-11-25 (no vendor document was read for this claim)
---

## Claim

A `quartus_map` (Analysis and Synthesis only) run of one entity is a cheap way to rank the logic cost of individual features, but it is not a fit: it has no packing, no timing and no placement. In one calibration it matched the fitted figure for block memory bits exactly (the entity's block bits plus the separate line buffer equalled the fitted total), matched the DSP count, and landed within about 5 percent of the fitted ALM count; its derived M10K count was only a floor because the fitter shapes wide memories differently from a bits-divided-by-block-size model.

## Evidence

First-hand, one core under test, 2026-11-25: the entity as built for the shipped release mapped to about 1,489 ALMs, 6 DSP and 221,696 block bits; adding the 16,384-bit scan-out line buffer gave exactly the 238,080 bits of the earlier fitted module, and the DSP count (6) matched; the ALM estimate plus the scan-out module was within about 5 percent of the fitted 1,532. Compiling out one feature at a time on a scratch copy gave additive deltas (four features summed within 4 ALMs of the all-on build) and an all-features-off build within 8 ALMs of the release build. Each map run took 3 to 4.5 minutes on an emulated x86 VM. One entity, one device, one calibration point.

## How to validate on hardware

Not a hardware question: for your own core, map the entity alone, then compare with the fitted per-entity numbers in the fit report of a closed build (Fitter > Resource Utilization by Entity). Use map deltas only to rank options; take the final numbers, timing and the LAB packing from a fit.
