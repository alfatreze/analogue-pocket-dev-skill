---
id: KB-082
title: Measure a real-silicon CDC's timing with a single-bit toggle + destination-domain counter -- no JTAG session needed
status: hardware-validated
confidence: high
first_seen: 2026-10-01
last_verified: 2026-10-01
tags: [cdc, clock-domain-crossing, jtag-alternative, diagnostic, firmware-mmio, local-technique]
applies_to: any design that needs to verify a clock-domain-crossing's real-silicon timing behaviour
  (not just simulated behaviour) without setting up a live JTAG/SignalTap session
evidence: Real hardware: minimum measured intervals of an I2S clock-domain crossing matched CLK_HZ/sample_rate almost exactly at 44.1 kHz (1508 vs 1511.7 ideal) and 48 kHz (1383 vs 1388.9 ideal), across a fresh core restart.
sources:
  - developer hardware measurement, 2026-10-01 (project-internal)
---

## Claim
To check whether a CDC behaves on real silicon the way simulation predicts, a live JTAG probe session
is not the only option and is often not the best one (JTAG polling is too slow to catch fast events,
and needs a physical session with a cable attached). A cheaper, firmware-readable alternative: flip a
single bit in the SOURCE domain on every event of interest, synchronise that one bit into the
DESTINATION domain with a plain 2-3 stage flip-flop chain (safe for a single bit -- see the Gray-code
caveat below), then do ALL further measurement (edge detection, interval timing, min/max/count/sum)
entirely within the destination domain against its OWN free-running cycle counter. This needs no
multi-bit CDC handling at all past the single synchroniser, is exposed as plain read-only MMIO
registers, and can be read any time via the normal diagnostics/Info-page mechanism most designs
already have -- no cable, no live session.

**Important distinction:** this ONLY works safely for a single bit. A multi-bit value (e.g. a
free-running counter's full width) crossing domains needs Gray-coding or a different technique,
because multiple bits can appear to change on the same source edge and a plain synchroniser cannot
safely resolve which combination was actually on the register at any one destination-domain sample.

## Evidence
One core needed to verify an I2S audio CDC (`sync_fifo`/`dcfifo`, already simulated clean twice with
both a behavioural model and the vendor's own `dcfifo` simulation model) on REAL silicon, since
simulation checks logical values, not real inter-edge timing, and a prior MCLK-generator
investigation had already found a real jitter bug that only ever showed up on hardware. Built: a
single-bit toggle in the source domain, flipped whenever the CDC's output value changed; a plain
3-stage synchroniser into the destination domain (reusing an existing generic single-bit-sync module);
interval/min/max/count measurement entirely in the destination domain against that domain's own
free-running cycle counter; exposed as 4 new read-only MMIO registers; surfaced on an existing
diagnostics page. Result: minimum measured intervals (the signal immune to idle-gap/burst
contamination) matched the theoretical ideal almost exactly at two different sample rates, on real
hardware, across a fresh power-on -- the same confidence a live JTAG capture would have given, at a
fraction of the setup cost, and reusable on any future boot without a cable.

## How to validate on hardware
Build the toggle + synchroniser + destination-domain measurement, expose via MMIO, read via whatever
diagnostics mechanism the design already has. Compare the MINIMUM measured interval (not the average,
which can be contaminated by legitimate idle periods, and not the maximum, which saturates on any long
pause) against the theoretical ideal interval for the event rate being measured. A close match across a
power cycle is strong real-silicon evidence the crossing is clean; a mismatch is the first direct
hardware evidence of a real problem simulation could not have caught.
