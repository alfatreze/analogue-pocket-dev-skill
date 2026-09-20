---
id: KB-013
title: Link port and cartridge pins require cartridge_adapter 0 and link_port true; all link lines are bidirectional; about 6 MHz limit
status: community-reported
confidence: medium
first_seen: 2026-09-20
last_verified: 2026-09-20
tags: [io, link-port, cartridge]
applies_to: observed with a scope by agg23
sources:
  - https://github.com/agg23/analogue-pocket-utils/wiki/IO
  - https://github.com/agg23/openfpga-litex
---

## Claim
To use the link port set both `link_port: true` and `cartridge_adapter: 0` (which also powers the cart port). Template comments about lines being input-only are GBA-specific; all four lines work bidirectionally. Signal integrity degraded above about 6 MHz. The dev-kit UART cart also needs cartridge_adapter 0. Cartridge_adapter -1 leaves power off.

## Evidence
agg23 wiki IO page; LiteX README.

## How to validate on hardware
Loopback test with a known pattern at 1, 3 and 6 MHz.
