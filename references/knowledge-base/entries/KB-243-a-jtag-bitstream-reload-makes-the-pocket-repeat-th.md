---
id: KB-243
title: A JTAG bitstream reload makes the Pocket repeat the whole load with the same starting conditions, so reflash-and-retest can run unattended; only selected assets survive
status: docs-verified
confidence: low
first_seen: 2026-11-11
last_verified: 2026-11-11
tags: [jtag,iteration,reload,heartbeat,automation]
applies_to: all framework versions; per the Analogue developer docs
evidence: docs: getting-started, overview, bus-communication, changelog 1.1 beta 5/6 (2026-11-11)
sources:
  - https://www.analogue.co/developer/docs/getting-started
  - https://www.analogue.co/developer/docs/overview
  - https://www.analogue.co/developer/docs/bus-communication
---

## Claim
Reloading the FPGA bitstream over JTAG makes the Pocket repeat the whole core load automatically with the exact same starting conditions. Previously selected assets are remembered and reloaded, JSON files are re-read (so edits between reloads take effect), and all other stateful data is not carried over. The Pocket notices a reload because the PAD bus heartbeat stops. Together this allows an unattended reflash-and-retest loop from a PC with a JTAG cable. Chip32 handling: a JTAG reload makes the CORE instruction be skipped and Chip32 reinitialises (changelog 1.1 beta 5 and beta 6).

## Evidence
Docs, getting-started: "After a core is running the developer can at any time reload the FPGA bitstream over JTAG. Pocket will automatically re-initialize the core with the exact same starting conditions." Docs, overview (Developing a Core) and bus-communication (heartbeat: "When a dev reloads core using JTAG, Pocket will detect the loss of signal and reload the core with the same start conditions"). Changelogs 1.1 beta 5 and beta 6 for Chip32.

## How to validate on hardware
Reload a known bitstream three times with quartus_pgm and time each reload until the core is running; edit a JSON value between reloads and confirm it is picked up; confirm that any RAM or save content the core held is gone after reload. Record the reload time and whether a data-slot load repeats.
