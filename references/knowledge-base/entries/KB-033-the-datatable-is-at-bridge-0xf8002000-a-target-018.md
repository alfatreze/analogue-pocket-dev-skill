---
id: KB-033
title: The datatable is at bridge 0xF8002000; a target 0184 using a wrong bridge base completes with result 0 but stores zeros
status: community-reported
confidence: medium
first_seen: 2026-09-19
last_verified: 2026-09-20
tags: [bridge, datatable, target-commands, hardware]
applies_to: one core, one Pocket, firmware and framework version not recorded
sources:
  - https://www.analogue.co/developer/docs/host-target-commands
  - Hardware observation by the skill author, 2026-09-19 (no public artifact)
---

## Claim
The data-slot ID/size table is reachable on the bridge at `0xF8002000`: table word N is at `0xF8002000 + 4*N`. A target write (0184) whose bridge-address argument used `0xF8000000 + 4*N` did not read the table: the destination slot received zeros while the command still completed with result code 0.

## Evidence
The docs place the table at offset 0x2000 from the 0xF8000000 base. Observed: the core's own table words were correct locally, the 0184 reported result 0, but reading the slot back with 0180 returned `00000000` and the saved file stayed zero. Changing only the base constant to `0xF8002000` made the same read return the expected words. Result 0 therefore means the transfer finished, not that the address was meaningful.

## How to validate on hardware
Put a known word at table word 200, issue 0184 with bridge address `0xF8002000 + 200*4` and again with `0xF8000000 + 200*4`, read each back with 0180 into other words, and compare.
