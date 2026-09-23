---
id: KB-050
title: Quartus Lite 25.1 applies register retiming and duplication on Cyclone V, contrary to a secondary claim that Lite lacks register retiming
status: disputed
confidence: medium
first_seen: 2026-09-23
last_verified: 2026-09-23
tags: [quartus, cyclone-v, toolchain, fitter, editions, edition-claim]
applies_to: Quartus Prime Lite 25.1std.0 Build 1129, Cyclone V 5CEBA4F23C8; the classic Fitter physical-synthesis options
evidence: A Lite 25.1 fit report of a Cyclone V design shows the options ON and 1,132 Retimed Register entries in the physical-synthesis netlist changes
sources:
  - https://en.wikipedia.org/wiki/Quartus_Prime
  - Quartus Lite 25.1std.0 Build 1129 fit report of a Cyclone V 5CEBA4F23C8 design (local artifact, not public)
---

## Claim
Wikipedia (repeated by several search summaries) says the Lite edition "lacks ... register retiming". For the classic Fitter physical-synthesis options on Cyclone V this is not true in Lite 25.1: with `PHYSICAL_SYNTHESIS_REGISTER_RETIMING`, `_REGISTER_DUPLICATION` and `_COMBO_LOGIC` set ON, the fit report lists them as On and records the fitter retiming registers. The Wikipedia statement probably refers to newer Pro-only Hyper-Retiming-style features. Treat any "edition X lacks feature Y" claim as unverified until a report from your own edition shows it.

## Evidence
Fit report header: "Quartus Prime Version 25.1std.0 Build 1129 10/21/2025 SC Lite Edition". Fitter Settings: Perform Register Retiming for Performance = On, Register Duplication = On, Physical Synthesis for Combinational Logic = On, Physical Synthesis Effort Level = Normal, Fitter Effort = Auto Fit. The physical-synthesis netlist-change table contains 1,132 entries labelled "Retimed Register". Scope: one design, one build; Intel's own edition comparison was not readable (HTTP 403), so the Wikipedia claim could not be traced to its primary source.

## How to validate on hardware
Run `python3 scripts/refresh.py edition path/to/ap_core.fit.rpt` on your own Lite build: a nonzero "registers retimed" count with the option ON means retiming is applied.
