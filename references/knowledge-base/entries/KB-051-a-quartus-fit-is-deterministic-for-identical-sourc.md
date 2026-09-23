---
id: KB-051
title: A Quartus fit is deterministic for identical source and seed, but bitstreams are not byte-identical because the framework stamps build_id.mif on every compile
status: community-reported
confidence: low
first_seen: 2026-09-23
last_verified: 2026-09-23
tags: [quartus,cyclone-v,timing,seed,build,process]
applies_to: Quartus 18.1 in the community Docker image used for Pocket builds (edition not stated by the source), Cyclone V; other versions untested
sources:
  - https://github.com/plasticbugs/pocket-core-template/blob/main/METHODOLOGY.md
---

## Claim
One community core's methodology reports that the same container and the same source gave the same timing slack to three decimals on a laptop and in CI every time, so a local compile predicts what a CI compile will do and can be inspected afterwards with quartus_sta. It also reports that the resulting bitstream differs on every compile because the APF framework stamps date, time and a random id into build_id.mif. Consequence: a CI rebuild that passed timing is a twin of the tested binary, not that binary; release the exact bitstream that was tested. Complements the seed-variation entry (KB-011): variation is across seeds, not across repeats of the same seed.

## Evidence
Source (author's own account, one project, Quartus 18.1 image, dates 2026-09): "the same slack to three decimals on my machine and in CI, every time - and a different bitstream, because the framework stamps the date, the time and a random id into build_id.mif on every compile." Not independently reproduced here; the page was read in full, the claim was not tested.

## How to validate on hardware
Compile the same tree twice with the same seed and compare (a) the setup/hold slack in the timing report and (b) the RBF hashes. Expect identical slack and different RBF hashes. If the slacks differ between repeats, machine load or thread count is affecting your fit and the claim does not hold for your setup. Only the framework's build id file should differ: diff the two RBFs to confirm the difference is confined to it.
