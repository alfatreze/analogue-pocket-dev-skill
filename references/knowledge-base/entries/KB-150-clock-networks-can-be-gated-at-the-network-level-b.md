---
id: KB-150
title: Clock networks can be gated at the network level, but a network that drives a PLL cannot be dynamically enabled or disabled
status: docs-verified
confidence: medium
first_seen: 2026-10-13
last_verified: 2026-10-13
tags: [clocking,clock-gating,power,cyclone-v]
applies_to: Cyclone V E (5CEBA4F23C8, the Analogue Pocket FPGA), Quartus Prime Lite or Standard; Cyclone V Device Handbook Vol 1 as served on docs.altera.com, read 2026-10-13
sources:
  - Cyclone V Device Handbook Volume 1 (docs.altera.com), handbook ch.4: 4.1.8, 4.1.9; ch.2: 2.2.5
---

## Claim
Unused GCLK, RCLK and PCLK networks are powered down automatically by configuration bits. The clkena signal gates a clock at the clock-network level (not per PLL output counter), so it works even without a PLL, but it cannot be used on a GCLK or RCLK that drives a PLL input. Memory blocks add a read-enable that skips unnecessary reads and lowers dynamic power, and Quartus puts unused memory blocks in low-power mode.

## Evidence
Handbook sections 4.1.8 (clock power down), 4.1.9 (clock enable signals) and the memory power guideline 2.2.5.

## How to validate on hardware
Use ALTCLKCTRL (or the equivalent inferred clock-enable) for gating decisions, and check the clock-network report to confirm which network each gated clock lands on.
