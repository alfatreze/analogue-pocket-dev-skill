---
id: KB-018
title: Devkit debug cart and SignalTap tips
status: community-reported
confidence: medium
first_seen: 2026-09-20
last_verified: 2026-09-20
tags: [debug, signaltap, devkit]
applies_to: unspecified
sources:
  - https://github.com/agg23/analogue-pocket-utils/wiki/Quartus
  - https://github.com/agg23/analogue-pocket-utils/wiki/Devkit---Debug-Key
---

## Claim
Devkit debug key: SiLabs CP2104 USB-UART up to 2 Mbps, LED, button; needs cartridge_adapter 0 (cart power), uses bank0 as output and bank3/pin31 as inputs. SignalTap: keep several instances, use lock mode to change triggers without recompiling, and use Pause Core Boot / Pause Load Data to arm early triggers. Do not use clone USB Blasters (reported to have killed a Pocket). Newer Quartus needs pll_wizard.lst edited for megafunction versions.

## Evidence
agg23 wiki Quartus and Devkit pages; LiteX README (clone warning).

## How to validate on hardware
Not yet designed.
