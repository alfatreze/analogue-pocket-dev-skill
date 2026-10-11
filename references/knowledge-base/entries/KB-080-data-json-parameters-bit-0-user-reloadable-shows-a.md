---
id: KB-080
title: data.json parameters bit 0 (User-reloadable) shows a Reload action per slot -- easy to leave set by copy-paste default
status: hardware-validated
confidence: high
first_seen: 2026-09-30
last_verified: 2026-09-30
tags: [data-json, parameters-bitmap, ui-cleanliness, apf, local-technique]
applies_to: any openFPGA core with data slots, especially ones scaffolded from a template
evidence: Real hardware: unwanted "Load Audio File"/"Load Playlist" actions in Core Settings; all 7 non-firmware data slots carried the same parameters value 0x1. Clearing bit 0 on all seven removed every unwanted action.
sources:
  - Analogue core-definition-files docs (data.json page), Parameters Bitmap table, bit 0
---

## Claim
`data.json`'s per-slot `parameters` field is a bitmap; bit 0 is "User-reloadable" and its ONLY visible
effect is adding a "Reload <slot name>" action to the Pocket's Core Settings menu. It is easy for every
data slot in a core to end up with the exact same `parameters` value (e.g. `"0x1"`) via copy-paste
from a template or from the first slot written, without anyone deliberately deciding each slot should be
user-reloadable. The result is a Core Settings menu cluttered with reload actions for things that were
never meant to be user-triggered (firmware-internal assets: loading-screen artwork, an index file, a
cold-code image, an assets bundle, a cover-image slot) -- and, per KB-079, these slots also count toward
the documented combined interact+data 20-entry menu budget, so an unintentionally-set bit here can
crowd out unrelated interact.json persist variables.

## Evidence
One core's `data.json` had 7 non-firmware slots (audio file, playlist, loading artwork, library index,
cold image, assets bundle, cover image) -- ALL flagged `parameters: "0x1"`. The developer had only
consciously noticed two of them ("Load Audio File"/"Load Playlist", both superseded by a later
direct-load/library feature) but the other five (loading artwork, library index, cold image, assets,
cover image) were equally exposed as manual reload actions despite being pure firmware-managed
internals with no legitimate user-facing reload use case. Clearing bit 0 on all seven (`"0x0"`) removed
every one of these unwanted actions and was hardware-confirmed correct.

## How to validate on hardware
Open the Core Settings menu on a real Pocket (or check `data.json` directly) and list every slot with
`parameters` bit 0 set. For each, ask whether a user genuinely needs a manual "reload this file" action
at runtime -- most firmware-internal assets (splash art, index files, cold-code images) do not, even
though a template or an early slot declaration may have set the bit by default.
