---
id: KB-255
title: A core can have the Pocket create a missing nonvolatile file: parameters bit 5 plus the core writing the slot's size-table entry
status: hardware-validated
confidence: low
first_seen: 2026-11-23
last_verified: 2026-11-23
tags: [save,nonvolatile,size-table,first-file]
applies_to: one core under test, Pocket firmware as of 2026-11; framework version not recorded
evidence: The same core and the same Pocket, two runs (2026-11-22/23): with the size entry left at 0 nothing was written; with the entry set to 8192 by the core the Pocket created the file. Confirmed by the Report rows (loaded words 2048, entry 0 at a first boot, 8192 once the file exists), by recreating the file after deleting it, and by two release cores of the same project.
sources:
  - https://www.analogue.co/developer/docs/core-definition-files/data-json
---

## Claim

The exit flush never creates a missing nonvolatile file by itself when the slot's size-table entry is 0, but a core can make the Pocket create it: set data-slot parameters bit 5 (initialise: a missing file fills the slot memory with 0xFF up to `size_maximum`, delivered through the bridge writes) and **write the file size into the slot's entry of the Dataslot ID/Size Table** (word 2i+1) after boot. At the next Quit or at a direct power-off the Pocket then writes that many bytes and the file appears under `/Saves/<platform>/<core>/`. The entry of a slot that was never loaded exists and reads 0; once a file exists APF fills the entry itself. No core-issued target data-slot write is needed. This is what makes a shipped seed file unnecessary.

## Evidence

Measured on a Pocket with a core under test: with bit 5, no file and the entry left at 0, edits were lost and no file was created; with the core writing 8192 into the entry on the first edit, the Pocket created the 8192-byte file at a direct power-off, loaded it at the next boot, and recreated it after it was deleted. The Report rows read at the first boot with no file: loaded words 2048, size entry 0. Release cores of the same project repeated it. This refines KB-074 claim 1 (flush never creates the first file) and supports KB-001.

Where the file lives and how it loads (same core, hardware): a core-specific nonvolatile slot (parameters bit 1) is `/Saves/<platform_ids[0]>/<author.core>/<filename>` (a development core on a second platform id used `/Saves/<that platform>/<core folder>/`); at boot the Pocket delivers the file as bridge writes at the slot's `address` before the core's all-complete, which a core can count (2,048 words for an 8,192-byte file); it reads the same range back with bridge reads at Quit and at a direct power-off.

## How to validate on hardware

With bit 5 set and no file, write the file size into the slot's size-table entry from the core (address word 2i+1 where word 2i holds the slot id), change the save RAM, power off, and look for the file on the card. Repeat with the entry left at 0 to see nothing written.
