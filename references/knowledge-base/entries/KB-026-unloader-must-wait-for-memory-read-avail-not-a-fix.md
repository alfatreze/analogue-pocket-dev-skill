---
id: KB-026
title: Unloader must wait for memory read_avail, not a fixed delay: a fixed-delay save read returns default or stale words (all-zero save body)
status: community-reported
confidence: medium
first_seen: 2026-09-20
last_verified: 2026-09-20
tags: [save,bridge,flush,psram,data_unloader]
applies_to: K3V GBA core v0.1.5 (2026-08), one project audit; the "upstream unloader" it patched was not inspected by us
sources:
  - https://github.com/K3v-68/k3v-gba/blob/main/AUDIT_REPORT.md
  - https://github.com/K3v-68/k3v-gba/blob/main/src/fpga/core/core_top.sv
---

## Claim
A core that serves APF's save flush (bridge reads through agg23's `data_unloader`) from memory with variable latency (PSRAM) must return data only after the memory says the word is valid (`read_avail`), and the bridge must stall until the whole 32-bit response exists. Sampling the memory after a fixed cycle delay lets a busy or delayed access put a default or stale word into the response path, which shows up as a save file that is zero except where another path (here the RTC footer mux) supplies data.

## Evidence
K3V AUDIT_REPORT.md, "Save-path audit and fixes": "The upstream unloader sampled PSRAM after a fixed cycle delay instead of waiting for `read_avail`. A delayed/busy PSRAM access could therefore place the default or stale word into the Pocket response FIFO." and "matching the reported failure signature of an all-zero 128 KiB body with an intact final 16-byte RTC extension." The fix uses request/ready and response/valid handshakes; "A missing PSRAM response can no longer be converted into zero data." Code: `src/fpga/core/core_top.sv` comment "The unloader expects fixed-latency reads. We use a small FSM to bridge the unloader's read_en/read_data interface to the PSRAM's busy/read_avail." Scope: one project's own audit, PSRAM, v0.1.5, 2026-08-14.

## How to validate on hardware
