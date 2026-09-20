---
id: KB-009
title: Multi-bit clock-domain crossings must not use a per-bit synchronizer chain
status: community-reported
confidence: high
first_seen: 2026-09-20
last_verified: 2026-09-20
tags: [cdc, timing]
applies_to: engineering fundamental; stated by a prolific Pocket core author
sources:
  - https://github.com/agg23/analogue-pocket-utils/wiki/Clocks
  - https://github.com/agg23/analogue-pocket-utils/blob/master/ip/sync_fifo.sv
---

## Claim
A flop chain (like APF's `synch_3`) is only safe for single-bit signals. Passing a bus through per-bit chains can yield stable but wrong values (00 -> 11 may appear as 10). Use a dual-clock FIFO, a handshake, or gray coding for buses. Analogue's example code does bus crossings this way anyway.

## Evidence
agg23 wiki (Clocks). Also standard CDC theory. Clocks with a common integer divisor are effectively synchronous.

## How to validate on hardware
Audit every multi-bit signal crossing between clk_74a and PLL domains (bridge address/data, status, table writes) for per-bit synch_3 use; replace with sync_fifo or handshake and re-run.
