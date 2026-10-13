---
id: KB-153
title: Cyclone V I/O pins have per-pin slew rate, drive strength, output delay, open-drain, bus-hold and pull-up controls; some are mutually exclusive
status: docs-verified
confidence: medium
first_seen: 2026-10-13
last_verified: 2026-10-13
tags: [io,slew-rate,pull-up,bus-hold,timing,cyclone-v]
applies_to: Cyclone V E (5CEBA4F23C8, the Analogue Pocket FPGA), Quartus Prime Lite or Standard; Cyclone V Device Handbook Vol 1 as served on docs.altera.com, read 2026-10-13
sources:
  - Cyclone V Device Handbook Volume 1 (docs.altera.com), handbook ch.5: 5.8 (Table 49, 5.8.1 to 5.8.9)
---

## Claim
Per pin: slew rate 0 (slow) or 1 (fast, default), disabled when on-chip series termination is used; programmable output buffer delay of 0 (default), 50, 100 or 150 ps, with independent rising and falling edge control (usable to trim duty cycle, skew, simultaneous-switching noise or memory-interface margin); open-drain output via the OPNDRN primitive or the Auto Open-Drain Pins option (writing an ordinary tri-state does not use the dedicated open-drain feature, which gives the best OE-to-output delay); bus-hold (about 7 kohm nominal, active only after configuration, holds the last driven state) or weak pull-up, which cannot both be on; on-chip clamp diode (recommended for 3.3 V standards, default off except PCI). A programmable IOE input/output delay can be applied to pins to meet hold or trim setup, and the datasheet gives its values. Pull-up and bus-hold apply to user I/O only; dedicated configuration, clock and JTAG pins have fixed internal pull-ups. The handbook recommends simulating before choosing slew and strength.

## Evidence
Table 49 and sections 5.8.1 to 5.8.9 of the handbook chapter on I/O features.

## How to validate on hardware
To change a margin on a source-synchronous bus (for example an SDRAM or PSRAM interface) add the delay or slew assignment to the pin in the .qsf and confirm the fit report and timing analysis changed; undriven bidirectional pins that float during tri-state are candidates for bus-hold or a pull-up.
