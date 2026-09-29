---
id: KB-074
title: A nonvolatile slot is only written back if it was loaded; the core must create the first save file itself with a target data-slot write
status: community-reported
confidence: medium
first_seen: 2026-09-29
last_verified: 2026-09-29
tags: [save,nonvolatile,target-commands,size-table]
applies_to: community arcade cores built from plasticbugs/pocket-core-template (Punch-Out, NBA Jam), 2026-09; Pocket firmware version not stated
sources:
  - https://github.com/plasticbugs/pocket-core-template/blob/HEAD/METHODOLOGY.md
---

## Claim

A community methodology document (section 5.24) says:
1. The exit-time flush only writes back a nonvolatile slot that was loaded. If no save file exists yet, the
   exit flush never creates one. The core must issue `target_dataslot_write` itself: a few seconds after the
   game last touches battery RAM, when the menu opens, and once a few seconds after loading.
2. The save slot's size must be in the data-slot size table at entry `position*2+1`, where position is the
   slot's place in data.json. A zero entry means nothing is written. This agrees with KB-001.
3. Set parameters bit 5 (initialise the slot if the file is missing). Otherwise a never-loaded slot has no
   filename for the core's write.
4. In that template, putting the save slot at bridge address 0x10000000 "hangs the load the moment a file
   exists". It uses 0x20000000, with its own loader and unloader. Treat this as specific to that template's
   address decoding, not a platform rule.
5. The load path and the write path are separate RTL. When a slot id moves (for example after adding a
   game-list JSON slot 0), every comparison against the id has to move with it. Otherwise saves are written
   but never reloaded.

## Evidence

One source, the template repository's METHODOLOGY.md (commit of 2026-09-25, section 5.24), describing
fixes that each "cost a hardware round" on the author's cores. Quote: "The Pocket only writes back a slot
it *loaded*, so the exit-time flush can never create the first file." Not independently confirmed. It
touches KB-005 (target write reliability is disputed) and KB-003 (64 KB delivery limit).

## How to validate on hardware

With no save file on the card, run a core that has a nonvolatile slot and parameters bit 5 set, but never
issues a target write. Change battery RAM, then Quit. Check whether `/Saves/<platform>/...` gains a file.
Repeat with a core-issued target write. Then use the source's three-step check: the file exists, its
contents differ from the factory image where you changed something, and the change survives quitting and
relaunching the core.
