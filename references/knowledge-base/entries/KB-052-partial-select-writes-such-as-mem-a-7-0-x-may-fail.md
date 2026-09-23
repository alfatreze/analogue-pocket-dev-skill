---
id: KB-052
title: Partial-select writes such as mem[a][7:0] <= x may fail to infer Quartus byte enables and explode into registers; use packed 2D arrays and word-buffered writes
status: community-reported
confidence: low
first_seen: 2026-09-23
last_verified: 2026-09-23
tags: [quartus,cyclone-v,memory,m10k,inference]
applies_to: Quartus 18.1 in the community Docker image used for Pocket builds (edition not stated by the source), Cyclone V; behaviour in Lite 25.1 untested
sources:
  - https://github.com/plasticbugs/pocket-core-template/blob/main/METHODOLOGY.md
---

## Claim
In one community template's methodology, partial-select writes to a memory word (for example `mem[a][7:0] <= x`) did not infer byte enables and the memory was built from registers instead of block RAM. The recommended pattern is a packed 2D array (`logic [1:0][7:0]`) written a whole word at a time, so the byte-enable form is recognised. Treat as a lead: check the synthesis RAM report before trusting a memory to have landed in M10K.

## Evidence
Source (same document, section on SD/RTL pitfalls): "partial-select writes like `mem[a][7:0] <= x` fail to infer byte enables in Quartus and explode into registers. Use 2D-packed (`logic [1:0][7:0]`) and word-buffered writes." Read in full; no synthesis run to confirm. Scope: the author's arcade cores, Quartus 18.1.

## How to validate on hardware
Compile a small module both ways with quartus_map and compare the Analysis & Synthesis RAM Summary (M10K/MLAB block count) and the register count. Record the Quartus version and edition string from the report header. If Lite 25.1 infers byte enables for both spellings, mark this entry refuted for that version.
