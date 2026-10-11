---
id: KB-056
title: Manually copied cores need the Pocket's five catalog caches cleared to appear in the menu
status: hardware-validated
confidence: high
first_seen: 2026-09-20
last_verified: 2026-09-23
tags: [sd-card,packaging,menu,catalog-cache]
evidence: A core installed by file-drop was missing from the Pocket's menu; the five System/*.bin cache files predated every install of that session. Clearing them is a step the developer's standing install procedure had followed for dozens of installs before one session skipped it. Two other theories (a non-standard core.json version string, an over-length description) were tried first and did not fix it.
applies_to: any core installed by copying files directly onto the SD card (the `Cores/<author>.<shortname>/` + `Assets/<platform>/` + `Platforms/<platform>.json` file-drop workflow), not through the Pocket's own USB SD Access add/remove flow
sources:
  - developer card-install history, 2026-09-20 to 2026-09-23 (project-internal)
---

## Claim

The Pocket keeps five cache files under `/System/` on the SD card that describe the current core/platform
catalog for the menu:

- `core_viewby_platform.bin`
- `corelist_cache.bin`
- `cores_cache.bin`
- `platform_viewby_category.bin`
- `platforms_cache.bin`

**A core added by copying files directly onto the card does not reliably appear in the menu until these five
files are deleted**, so the Pocket rebuilds them from a fresh scan on its next boot/card reinsertion. The
failure mode is completely silent: no error, no log entry visible to the user, the core simply isn't in the
list -- indistinguishable from a genuinely broken `core.json` or a missing platform file (the actual failure
mode `sd-packaging-assets.md` already documents for a different cause).

## Evidence

The developer followed a "backup the five caches, delete them, let the Pocket rebuild" step as a standing
part of every card install (dozens of installs on one Pocket). In one later session this exact step
was skipped for an entire session's worth of test-build installs (roughly a dozen card writes across several
hours) despite being part of the standing card-write procedure (backup / clear-catalog / verify-SHA-256 / eject) -- the result was a core that never appeared in the menu, misdiagnosed
twice as a `core.json` field-format problem (a non-standard `version` string, then an over-length
`description`) before the actual cause was checked and found: all five cache files present, with timestamps
predating every install attempted that session. Clearing them was the step that had actually been missing.

**Confidence caveat, stated honestly:** the developer treated cache-clearing as necessary across dozens of
installs, but no isolated A/B test exists (a matched pair of installs, cache cleared vs not, otherwise
identical) proving the cache alone -- rather than some other simultaneous variable in each of those installs --
is what makes the difference. Downgrade this from "high" confidence if a controlled test later shows a new
core CAN appear without clearing the cache under some condition (e.g. it may matter only when *renaming* or
*reusing* a platform id an earlier core already used, not for a genuinely fresh one -- every install in
that history has been exactly that kind of iterative reuse, never a completely virgin platform id).

## How to validate on hardware

1. **Controlled A/B, not yet done:** install a genuinely new core (fresh `author.shortname`/`platform`, never
   seen by this Pocket before) with the five caches deliberately left untouched; observe whether it appears
   in the menu after a normal reinsert/boot. Then delete the caches and observe again. If it appears both
   times, the caching theory is wrong or incomplete for the "new" case.
2. **Timing check:** is a stale cache actually stale by content (built before this core existed) or just by
   file mtime? A byte-level diff of the cache before/after a rebuild, correlated with what changed, would
   confirm the mechanism rather than inferring it from mtime alone.
3. **Whether the Pocket's own "Tools > Developer > Builds" list** (documented in `sd-packaging-assets.md`)
   shows a core that's present on the card but missing from the main menu -- if it does, that's a stronger,
   more direct diagnostic than clearing the cache and hoping.
