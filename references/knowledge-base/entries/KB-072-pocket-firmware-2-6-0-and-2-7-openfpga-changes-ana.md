---
id: KB-072
title: Pocket firmware 2.6.0 and 2.7 openFPGA changes; Analogue publishes a firmware-list API
status: docs-verified
confidence: high
first_seen: 2026-09-29
last_verified: 2026-09-29
tags: [firmware,changelog,openfpga-menu]
applies_to: Analogue Pocket OS firmware 2.6.0 (2026-06-17) and 2.7 (2026-09-04); no openFPGA framework version change
sources:
  - https://www.analogue.co/developer/docs/api
  - https://www.analogue.co/support/pocket/firmware/2.7/details
  - https://www.analogue.co/support/pocket/firmware/2.6.0/details
---

## Claim

Two Pocket OS releases since framework 2.3 changed openFPGA-facing behaviour without changing any
developer documentation text (the docs pages were re-read 2026-09-29 and their content is unchanged;
only their URLs moved under `/developer/docs/openfpga/`):

- **2.6.0 (2026-06-17), openFPGA:** a "Recent" category stores the most recent usage; quitting a core now
  returns to the openFPGA menu; the openFPGA menu opens faster when cached. **OS:** new Auto Dim and Auto
  Off power options (defaults 5 minutes and 2 hours), set under the PocketOS power settings. So screen
  dimming on idle is an OS function, not something a core controls.
- **2.7 (2026-09-04), openFPGA:** higher maximum platform/core count; pre-cached core lists load twice as
  fast. **General:** unplugging USB while a core runs is no longer unstable; faster USB connection.

Both releases lean on a cached core list. That fits the known need to delete the OS catalog cache files
after adding a core to the card, but neither note says whether that is still needed (see How to validate).

Analogue also documents a public read-only firmware API: `GET /support/pocket/firmware/list`,
`/support/pocket/firmware/latest` (307 redirect to the newest version) and
`/support/pocket/firmware/{version}/details` (JSON with release notes in Markdown and HTML, md5, size).
Use it to check the current firmware and its openFPGA notes instead of relying on news articles.

## Evidence

Release notes read directly from the vendor's details endpoint on 2026-09-29, for example 2.7:
"Improved: Increased maximum platform/core count" and "Pre-cached core lists now load twice as fast".
2.6.0: "Quitting a core now returns to the openFPGA menu". The API page is under the Analogue developer
docs (`/developer/docs/api`); its other new section, `/developer/docs/platform`, states it "currently only
applies to Analogue3D" and is not relevant to Pocket cores.

## How to validate on hardware

On firmware 2.7, add a new core to the card without deleting the catalog cache files and see whether it
appears in the openFPGA menu. That tells you whether the cache still has to be cleared on every install.
Record the firmware version with every hardware result from now on (Settings > System > firmware
version), since menu/cache behaviour changed in both releases.
