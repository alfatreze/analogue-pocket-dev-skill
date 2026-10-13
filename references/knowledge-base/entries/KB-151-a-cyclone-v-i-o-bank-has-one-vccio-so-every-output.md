---
id: KB-151
title: A Cyclone V I/O bank has one VCCIO, so every output in the bank drives that voltage; a 3.3 V bank can still accept 2.5 V and 3.0 V inputs
status: docs-verified
confidence: high
first_seen: 2026-10-13
last_verified: 2026-10-13
tags: [io,vccio,multivolt,levels,cyclone-v]
applies_to: Cyclone V E (5CEBA4F23C8, the Analogue Pocket FPGA), Quartus Prime Lite or Standard; Cyclone V Device Handbook Vol 1 as served on docs.altera.com, read 2026-10-13
sources:
  - Cyclone V Device Handbook Volume 1 (docs.altera.com), handbook ch.5: 5.3.4 (Table 35), 5.4.1
---

## Claim
Each I/O bank has its own VCCIO pins and supports a single VCCIO value (1.2, 1.25, 1.35, 1.5, 1.8, 2.5, 3.0 or 3.3 V). Non-voltage-referenced outputs in a bank always drive at VCCIO. Inputs are more tolerant: a bank at 3.3 V (VCCPD 3.3 V) accepts 2.5, 3.0 and 3.3 V inputs, and a bank at 2.5 V accepts 2.5, 3.0 and 3.3 V inputs while still driving only 2.5 V. VCCPD must be 2.5, 3.0 or 3.3 V and also powers the pre-driver of the output buffers (a higher pre-driver supply improves output performance). Voltage-referenced standards (SSTL, HSTL, HSUL) need a single VREF per bank and their inputs are powered from VCCPD. The handbook recommends an on-chip clamp diode for 3.0 or 3.3 V input signals. Consequence for a board design: a signal must be assigned to a bank whose VCCIO matches the voltage the receiving device needs, because the FPGA cannot drive a different level from the same bank.

## Evidence
Table 35 (MultiVolt I/O support) and the mixing rules in 5.4.1 of the handbook. Board-level facts about which Pocket pins sit in which bank come from the pin-out and schematic, not from this document.

## How to validate on hardware
Check the pin planner or fit report for each interface's I/O standard and bank VCCIO; a 3.3 V device (SDRAM, PSRAM, cartridge or link signals) must sit in a 3.3 V bank for its outputs to reach 3.3 V.
