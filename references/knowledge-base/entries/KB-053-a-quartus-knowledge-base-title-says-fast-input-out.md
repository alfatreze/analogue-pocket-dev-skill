---
id: KB-053
title: A Quartus knowledge-base title says FAST input/output/output-enable register assignments can be ignored when SignalTap is enabled (primary page not read)
status: community-reported
confidence: low
first_seen: 2026-09-23
last_verified: 2026-09-23
tags: [quartus,cyclone-v,signaltap,fitter,io]
applies_to: Quartus version and edition unknown (title of an Intel/Altera knowledge-base solution, age unknown), device family unknown; primary page not read
sources:
  - https://community.altera.com/kb/knowledge-base/why-is-my-fast-input-register-fast-output-register-or-fast-output-enable-registe/342446
---

## Claim
The title of an Intel/Altera knowledge-base solution asks why a Fast Input Register, Fast Output Register or Fast Output Enable Register assignment is ignored when the SignalTap logic analyzer is enabled in a design. If it applies to Cyclone V and to current Quartus, a build that combines SignalTap with FAST_*_REGISTER packing may silently lose the I/O-cell packing, so timing measured on the SignalTap build would not represent the shipping build. Lead only; the cause and resolution text were not read.

## Evidence
Source: search-result title of community.altera.com knowledge-base article 342446 (the old intel.com solution rd04172011_477 redirects there). The page returned HTTP 403, so only the title is known; there is no cause, version or device scope. Confidence low. Do not act on it beyond running the test below.

## How to validate on hardware
Build the same design twice with quartus_map plus quartus_fit, once with SignalTap enabled and once without, both with FAST_INPUT_REGISTER / FAST_OUTPUT_REGISTER / FAST_OUTPUT_ENABLE_REGISTER on some pins. In each fit report compare the I/O register packing (Resource Section, Input/Output Pins, 'Input Register' / 'Output Register' columns). Record Quartus version and edition. If packing is lost only in the SignalTap build, mark confirmed and keep timing sign-off on the non-SignalTap build.
