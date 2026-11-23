---
id: KB-254
title: A data slot with size_exact refuses a file of another size with a framework error screen and the core does not start
status: hardware-validated
confidence: low
first_seen: 2026-11-23
last_verified: 2026-11-23
tags: [save,nonvolatile,data-json,errors]
applies_to: one core under test, Pocket firmware as of 2026-11; framework version not recorded
evidence: A core under test on a Pocket (2026-11-23): an 8191-byte file for a size_exact 8192 slot produced Error in framework file id [11] size bad and a return to the core list at every start; deleting it restored start.
sources:
 - https://www.analogue.co/developer/docs/core-definition-files/data-json
---

## Claim

The data.json docs say a slot with `size_exact` is "only loaded if the size matches". On a Pocket the framework does not skip such a file silently: when a file of another size exists for the slot, the Pocket shows its own error screen, "Error in framework file id [N] size bad" (N = the slot id), and after a few seconds returns to the core list. **The core does not start** until the file is removed or replaced by one of the exact size. Plan for it: a save file that a user, a tool or a torn write leaves at another size makes the core unusable until it is deleted.

## Evidence

Observed by the owner of a core under test, 2026-11-23, on a Pocket with a nonvolatile slot (id 11, `size_exact` 8192, `size_maximum` 8192): the file cut to 8191 bytes produced the screen above at every start; deleting it restored normal start . A file of the exact size but of a newer content version loaded normally . Not tested: `size_maximum` alone (a larger or smaller file), a zero-byte file.

## How to validate on hardware

Put a file one byte short (or long) at the slot's save path and start the core; delete it and start again. Repeat with `size_exact` removed and only `size_maximum` set to see what a shorter and a longer file do.
