---
id: KB-028
title: Pocket data loader pushes a byte every 8 clocks and cannot be told to wait; a client that stalls (SDRAM refresh) needs a FIFO
status: community-reported
confidence: low
first_seen: 2026-09-20
last_verified: 2026-09-20
tags: [bridge,loader,sdram,fifo]
applies_to: plasticbugs pocket-core-template METHODOLOGY 5.16 (My Core hardware run, 2026-09); single source
sources:
  - https://github.com/plasticbugs/pocket-core-template/blob/main/METHODOLOGY.md
---

## Claim
The Pocket loader sends one byte every eight clocks into the core's download path and cannot be stalled. A download path that holds one pending word breaks when an SDRAM write sits behind a refresh: the next even byte lands in the high half of the word still waiting, so the image is peppered with bad words. A client that cannot stall needs a FIFO, and the simulation bench must push at the real rate.

## Evidence
METHODOLOGY.md 5.16: "The Pocket's loader sends a byte every eight clocks and *cannot be told to wait*." The first real-memory bench run used twelve clocks a byte and passed; at eight it "crashed exactly as the hardware did". Scope: the plasticbugs "My Core" arcade core on real hardware; the eight-clock figure is theirs, not from Analogue docs (not checked against official docs).

## How to validate on hardware
