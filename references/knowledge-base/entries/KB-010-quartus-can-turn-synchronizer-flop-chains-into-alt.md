---
id: KB-010
title: Quartus can turn synchronizer flop chains into ALTSHIFT_TAPS block RAM
status: community-reported
confidence: medium
first_seen: 2026-09-20
last_verified: 2026-09-20
tags: [cdc, quartus, synch_3, fitter]
applies_to: Quartus Lite; observed by one project (Paprium)
sources:
  - https://github.com/thekoalakoa/paprium-pocket/blob/master/docs/BUILD_REFERENCE.md
---

## Claim
With AUTO_SHIFT_REGISTER_RECOGNITION AUTO the fitter maps wide `synch_3` chains to ALTSHIFT_TAPS (M10K) instead of flops, defeating CDC. A global switch reached the narrow instances but not the wide ones (18 and 40 bit); a per-instance attribute is the proposed fix.

## Evidence
Paprium BUILD_REFERENCE 0.2.3 table: rd_chunk_synch (18b) and cont2_sync (40b) stayed block RAM; M10K dropped 286 to 281 instead of predicted 279.

## How to validate on hardware
Search the fitter report for ALTSHIFT_TAPS instances named after synchronizers; add `(* ramstyle = "logic" *)`/no-shift-register attributes on the stage registers and confirm M10K count changes.
