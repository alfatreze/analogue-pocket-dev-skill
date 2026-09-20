---
id: KB-019
title: Saves are named from the ROM path; renamed or moved ROMs orphan their save
status: community-reported
confidence: medium
first_seen: 2026-09-20
last_verified: 2026-09-20
tags: [saves, ux]
applies_to: unspecified
sources:
  - https://github.com/janisc/openfpga-NGPC
  - https://www.analogue.co/developer/docs/directories-and-sd-folder-structure
---

## Claim
With a slot flagged `nonvolatile filename` (param bit 2), the save path mirrors the slot-0 asset path under /Saves/<platform>/..., so two copies of a ROM in different folders keep separate saves and a rename orphans the save (rename the .sav to recover).

## Evidence
NGPC README plus Directories docs.

## How to validate on hardware
Not yet designed.
