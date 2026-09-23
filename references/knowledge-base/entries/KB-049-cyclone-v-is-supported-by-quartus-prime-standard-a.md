---
id: KB-049
title: Cyclone V is supported by Quartus Prime Standard and Lite but not Pro; the Pocket's Cyclone V builds in the free Lite edition
status: source-verified
confidence: high
first_seen: 2026-09-23
last_verified: 2026-09-23
tags: [quartus, cyclone-v, toolchain, editions]
applies_to: Quartus Prime versions 16.1 to 25.1 (Standard/Lite chart); Pro chart through 25.3
sources:
  - https://www.macnica.co.jp/en/business/semiconductor/articles/altera/95849/
  - https://github.com/janisc/openfpga-NGPC
---

## Claim
Cyclone V (including the 5CEBA4F23C8 in the Analogue Pocket) is supported by Quartus Prime **Lite** (free) and **Standard** (paid), and is **not** supported by **Pro**. So "Cyclone V works only in Lite" is not accurate (Standard also works), but for a free toolchain Lite is the only option, and Pro documentation, Pro-only features and Pro-only guidelines do not apply to this device. Lite also excludes larger families (Stratix, Arria); Cyclone 10 LP, Cyclone IV and MAX 10/V/II are Lite-supported.

## Evidence
The Macnica mirror of Altera's device-support chart has two tables. The Pro table lists only Agilex 7/5/3, Stratix 10, Arria 10 and Cyclone 10 GX. The Standard/Lite table shows Cyclone V as supported for both editions in every listed version from 16.1 to 25.1, while Stratix V/IV and Arria V/10 are Standard-only. The NGPC port's README states its Cyclone V 5CEBA4F23C8 design is verified with Quartus Prime Lite 17.1 and 25.1. Corroborated by several search summaries of Intel's edition comparison (Intel's own pages returned HTTP 403 to scripts, so the primary Intel table was not read).

## How to validate on hardware
Not hardware-related. Run `python3 scripts/refresh.py toolchain` to re-read the chart, and `python3 scripts/refresh.py edition path/to/ap_core.fit.rpt` to confirm your own builds report "Lite Edition".
