---
id: KB-032
title: A custom core FSM's target 0188 (flush) was never answered by Pocket within 10 s
status: community-reported
confidence: low
first_seen: 2026-09-19
last_verified: 2026-09-20
tags: [target-commands, flush, hardware]
applies_to: one core, one Pocket, firmware and framework version not recorded
sources:
  - Hardware observation by the skill author, 2026-09-19 (no public artifact)
  - https://www.analogue.co/developer/docs/host-target-commands
---

## Claim
When a core issued target command 0188 (data-slot flush) from its own `core_bridge_cmd` FSM (`target_0[15:0] = 0x0188`, slot id in the first parameter word), the Pocket never wrote a `0x6F6B` result within 10 s, even after a 0184 write to the same deferload slot had completed and read back correctly. An unanswered 0188 leaves the target bridge occupied: a following 0180 read on the same one-command-at-a-time bridge also timed out.

## Evidence
One negative observation. Earlier probes on the same core showed the same timeout at 0.5 s. Consistent with the official template never issuing 0188 (KB-007). This does not prove Pocket ignores 0188 in general: only one FSM implementation was tested, firmware/framework versions were not recorded, and the slot had no bridge `address`.

## How to validate on hardware
Repeat with a core that also logs the bridge; test a nonvolatile slot with a nonzero size-table entry and a bridge `address`; record firmware and framework versions; compare with an unmodified kbmouse-targetdata example (KB-005). A positive result from any public core would supersede this entry.
