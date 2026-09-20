---
id: KB-035
title: interact.json persist variables can carry a validated diagnostic record out of a core, stored as signed int32 when the core is Quit
status: community-reported
confidence: medium
first_seen: 2026-09-19
last_verified: 2026-09-20
tags: [interact, persist, diagnostics, hardware]
applies_to: one core, one Pocket, firmware and framework version not recorded
sources:
  - https://www.analogue.co/developer/docs/core-definition-files/interact-json
  - Hardware observation by the skill author, 2026-09-19 (no public artifact)
---

## Claim
A core can export a 64-byte result record through 16 `interact.json` `persist` variables of type `slider_u32` mapped to consecutive bridge addresses. APF reads the values back from the core and, when the user Quits the core to the menu, writes them to the interact persist JSON. The values are stored as SIGNED int32, so each word must stay below 2^31: a 32-bit record is carried as 15 words of the low 31 bits plus one word holding the withheld top bits. The file appeared under `Settings/<Author.Core>/Interact/_core/interact_persist.json` (the docs give `.../Interact/interact_persist.json`; treat the `_core` folder as observed, not documented).

## Evidence
The persist file decoded to a record whose XOR checksum matched the checksum computed by the firmware, and the on-screen readback words agreed with the file. Reads happen only after Quit: pulling the SD card without Quitting produced no file. The variables also appear as sliders in the Core Settings menu. Single core and unit; firmware not recorded.

## How to validate on hardware
Publish a distinctive word pattern with bit 31 set and clear, Quit from the menu, and decode the persist JSON; confirm the folder name on your firmware.
