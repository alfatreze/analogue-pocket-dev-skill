---
id: KB-242
title: Tools > Developer debug aids: Pause Core Boot, Pause Load Data, Debug Logging, Asset Load Detail, Statistics and USB SD access; the pause options have no effect when Chip32 runs
status: docs-verified
confidence: low
first_seen: 2026-11-11
last_verified: 2026-11-11
tags: [debug,developer-menu,signaltap,logging]
applies_to: all framework versions; per the Analogue developer docs (Debugging Aids, 2.3)
evidence: docs: debugging-aids page (read in full 2026-11-11)
sources:
  - https://www.analogue.co/developer/docs/debugging-aids
---

## Claim
Tools > Developer offers: Builds (lists installed cores even when the platform link is broken); USB SD Access (mounts the card over USB-C at about 700 KB/s; Analogue+X attaches, Analogue+Y detaches since 2.1); Statistics (an overlay with video sync rate to three decimals, sync status too low / too high / ok, temperature, and fabric power on Developer units); Pause Core Boot (halts right after the bitstream loads until A is pressed); Pause Load Data (halts before any data slot loads, so a SignalTap trigger can be armed on a data load); Asset Load Detail (file and slot being loaded; files under 512 KB may not show); Debug Logging (a detailed boot log in /System/Logs/); Chip32 Exec Log (every Chip32 instruction, which can slow boot a lot). Only the first two settings persist across power-off. Pause Core Boot and Pause Load Data have no effect when Chip32 runs.

## Evidence
Docs, Debugging Aids page (read in full for this entry).

## How to validate on hardware
Enable each option on a Pocket and note what appears. In particular check that Pause Load Data stops before the first slot write on a core with a Chip32 loader, to confirm it has no effect there.
