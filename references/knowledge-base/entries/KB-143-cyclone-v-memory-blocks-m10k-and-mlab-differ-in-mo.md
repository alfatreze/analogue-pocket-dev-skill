---
id: KB-143
title: Cyclone V memory blocks: M10K and MLAB differ in more than size, so check what the target block supports before choosing one
status: docs-verified
confidence: high
first_seen: 2026-10-13
last_verified: 2026-10-13
tags: [memory,m10k,mlab,cyclone-v,inference]
applies_to: Cyclone V E (5CEBA4F23C8, the Analogue Pocket FPGA), Quartus Prime Lite or Standard; Cyclone V Device Handbook Vol 1 as served on docs.altera.com, read 2026-10-13
sources:
  - Cyclone V Device Handbook Volume 1 (docs.altera.com), handbook ch.2: 2.1, 2.3 (Table 5, Table 6)
---

## Claim
The 5CEBA4 (member code A4) has 308 M10K blocks (10,240 bits each) and 303 MLABs (640 bits each, 32 x 20, ten ALMs per MLAB). Per the feature table: M10K tops out at 315 MHz and MLAB at 420 MHz. MLAB lacks packed mode, mixed-width ports and mixed-width FIFOs. MLAB supports simple dual-port, not true dual-port. MLAB is the only one of the two that can be read asynchronously (flow-through reads only). M10K single-port shapes run from 8K x 1 up to 256 x 40, with x32/x40 only at depth 256. MLAB is fixed at depth 32 with x16/x18/x20. Both support byte enables, parity bits, mixed-clock operation and .mif initialisation.

## Evidence
Table 1 (capacity per member), Table 5 (features) and Table 6 (single-port configurations) of the handbook's embedded-memory chapter. The 308 / 303 numbers match the block counts Quartus reports for the Pocket core. This is a manufacturer-documentation fact; it was not re-measured on hardware here.

## How to validate on hardware
Compare the RAM summary in the Quartus map/fit report for each memory (block type, width, depth) with Tables 5 and 6; a memory the report shows as logic, or as the wrong block type, usually asks for something the chosen block cannot do (true dual-port or mixed width on an MLAB, an unsupported width/depth combination).
