---
id: KB-161
title: Cyclone V checks the bitstream with a 16-bit CRC per frame during configuration and can check the loaded configuration RAM continuously in user mode
status: docs-verified
confidence: medium
first_seen: 2026-10-13
last_verified: 2026-10-13
tags: [seu,crc,error-detection,configuration,cyclone-v]
applies_to: Cyclone V E (5CEBA4F23C8, the Analogue Pocket FPGA), Quartus Prime Lite or Standard; Cyclone V Device Handbook Vol 1 as served on docs.altera.com, read 2026-10-13
sources:
  - Cyclone V Device Handbook Volume 1 (docs.altera.com), handbook ch.8: 8.1 to 8.4, 8.6
---

## Claim
During configuration the tool-generated bitstream carries a precomputed 16-bit CRC for each data frame; the device recomputes it as the frame loads and pulls nSTATUS low on a mismatch (so a corrupted or truncated bitstream is detected, and the Auto-restart option can retry). In user mode, an optional circuit (enabled under Device and Pin Options, Error Detection CRC) recomputes a 32-bit CRC for every frame of the configuration RAM against a precomputed value and drives the CRC_ERROR pin high on a mismatch; the 32-bit syndrome register is zero when clean, and a 67-bit error message register reports the type and location for single-bit and double-adjacent errors. Within a frame it detects all single- to quintuple-bit errors, and the handbook quotes 99.9999 percent detection overall. Detection runs until nCONFIG is pulled low. Optional internal scrubbing corrects single-bit and double-adjacent errors without reconfiguring, but only on parts with the SC suffix. The error detection feature does not affect fitting or performance. The CRC_ERROR pin can be open-drain, and when the feature is off the pin is a normal user I/O.

## Evidence
Sections 8.1 to 8.4 and 8.6 (Tables 107 and 108) of the handbook. Whether the Pocket connects the CRC_ERROR pin to anything a core can read is not documented here.

## How to validate on hardware
Corrupt a bit of a test bitstream and check that nSTATUS goes low during configuration; in user mode the handbook lists injecting an error through JTAG as a supported way to exercise the circuit.
