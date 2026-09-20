---
id: KB-004
title: Save flush is a bridge READ sequence at the slot's load address; a core can serve it from a demuxed address region
status: source-verified
confidence: medium
first_seen: 2026-09-20
last_verified: 2026-09-20
tags: [save, bridge, flush, data_unloader]
applies_to: observed on hardware by one project (NGPC)
sources:
  - https://github.com/janisc/openfpga-NGPC/blob/main/target/pocket/core_top.v
  - https://github.com/agg23/analogue-pocket-utils/blob/master/ip/data_unloader.sv
  - https://github.com/K3v-68/k3v-gba/blob/main/pkg/Cores/K3V.GBA/data.json
  - https://github.com/openfpgaOS/openfpgaSDK/blob/main/dist/sdk/Cores/ThinkElastic.openfpgaOS/data.json
---

## Claim
When APF flushes a nonvolatile slot it reads the slot back through ordinary bridge reads at the slot's `address` range. A core can serve these with agg23's `data_unloader` (address-mask select, fixed read latency) and produce a byte-perfect file.

## Evidence
NGPC: 'The flush reads arrive at the slot's address too'; 'APF never reads the BIOS or cartridge slots back, so every nibble-1 read is the save flush'; sim header states the flush READ leg 'produced a byte-perfect file on hardware'. Note the design uses PSRAM with bounded latency because a fixed read latency is only honest with bounded-latency memory.



## How to validate on hardware
Add a SignalTap or counter on `bridge_rd` with `bridge_addr` inside the save slot's address range during shutdown, and confirm reads occur (and how many) after Quit.
