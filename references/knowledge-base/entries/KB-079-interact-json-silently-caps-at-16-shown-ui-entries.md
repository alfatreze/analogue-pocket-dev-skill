---
id: KB-079
title: interact.json silently caps at 16 shown UI entries -- persistence for the 17th+ variable breaks too, no error anywhere
status: hardware-validated
confidence: high
first_seen: 2026-09-30
last_verified: 2026-09-30
tags: [interact-json, persist, ui-limit, apf, local-technique]
applies_to: any openFPGA core using interact.json persist variables
evidence: Real hardware: 17 declared interact.json variables made the two newest persist variables invisible in Core Settings and never saved; trimming to 14 fixed both on the same hardware and firmware.
sources:
  - Analogue core-definition-files docs (interact.json page): "Up to 16 UI entries from interact.json can be shown."
---

## Claim
Analogue's own interact.json documentation states plainly: "Up to 16 UI entries from interact.json can
be shown." This is not merely a display truncation -- on real hardware, adding a 17th (or later)
declared `variables` entry made those extra entries invisible in the Core Settings menu AND meant they
were never persisted to `interact_persist.json` on Quit, with no error, warning, or log line anywhere in
the toolchain. A previously-working set of persist variables was not affected; only the entries past the
16th silently stopped working. The doc separately names a second, related limit: "if more than 4
reloadable data slots are also present, additional entries will be dropped to maintain a maximum of 20
combined interact+data menu entries" -- i.e. data.json's own `User-reloadable` (parameters bit 0) slots
share pressure with this same budget.

## Evidence
One core's `interact.json` held 12 declared variables, all working. A firmware change added five new
persistable words (theme, theme mode, three meter presets) and their five matching `interact.json`
declarations were added too, bringing the total to 17 -- one over the cap. On real hardware: the two
new persist words did not show up in Core Settings at all (not "shown but not saving" -- genuinely
absent from the list), and confirmed via `interact_persist.json` inspection that they were never
written. Trimming back to 14 total entries (keeping only 2 of the 5 new ones, deferring the other 3)
immediately fixed both symptoms on the same hardware, same firmware otherwise unchanged -- confirmed hardware-visible and persisting correctly. This isolates the cause to the entry-count cap
specifically, not a coincidental unrelated bug in the same commit.

## How to validate on hardware
Count `interact.json`'s `variables` array length before adding new persist entries. If a core is already
near 16, either drop lower-priority entries to make room, or accept that anything past position 16 in
the array will silently do nothing -- no build error, no runtime error, no log line names the dropped
entry. If data.json also declares several `User-reloadable` (parameters bit 0) slots, budget against
the documented combined interact+data cap of 20, not just interact's own 16.
