---
id: KB-027
title: SDRAM data capture phase is a dial: measure setup and hold at two PLL phases at their worst corners, and fail the build on ignored SDC constraints
status: community-reported
confidence: medium
first_seen: 2026-09-20
last_verified: 2026-09-20
tags: [sdram,timing,quartus,pll]
applies_to: plasticbugs pocket-core-template METHODOLOGY 5.20 (My Core, Cyclone V 5CEBA4F23C8, commit 2ee52fc, 2026-09-19); single source
sources:
  - https://github.com/plasticbugs/pocket-core-template/blob/main/METHODOLOGY.md
---

## Claim
The SDRAM data pins into the controller capture register are a source-synchronous capture whose setup and hold trade against the SDRAM clock phase: shifting by 1 ns adds 1 ns to one slack and removes 1 ns from the other. A phase inherited from another core is a starting point only. Also, an SDC multicycle aimed at a register that Quartus merged away is silently dropped, so a constraint can claim a relaxation the analyzer never applied.

## Evidence
METHODOLOGY.md 5.20: "Setup on the SDRAM read gets `2T - shift` and hold gets `T - shift`: a nanosecond off the clock phase is a nanosecond onto one and off the other. Measure both slacks at two phase values, at the corner where each is worst (slow for setup, *fast* for hold), solve for where they meet, and round to a step the PLL can make." and "Fail the build on an ignored constraint... (332174 / 332049)". The report also warns that a `*0C*` corner match picks up the fast model and overwrote the slow one. Scope: one project, self-reported, no Pocket hold-slack numbers of ours.

## How to validate on hardware
