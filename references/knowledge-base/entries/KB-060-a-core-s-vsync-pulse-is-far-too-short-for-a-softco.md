---
id: KB-060
title: A core's vsync pulse is far too short for a softcore to poll: count frames in hardware
status: hardware-validated
confidence: high
first_seen: 2026-09-25
last_verified: 2026-09-26
tags: [video,vsync,softcore,cdc]
applies_to: a softcore (VexRiscv-class, single-threaded superloop, no interrupts) reading a vsync/vblank status bit through an MMIO register on the Analogue Pocket, video timing about 400x360 active at 60 Hz
evidence: Hardware: a polled vblank status bit read 0 edges per second on a Pocket; a free-running frame counter in the CPU clock domain read about 60 per second on the same wire, same firmware sampling window. Only the polled level versus the counter differed.
sources:
  - developer hardware measurement, 2026-09-25/26 (project-internal)
---

## Claim

A vsync pulse of 4 video lines (about 167 us at a 12 MHz pixel clock, 500 clocks per line) is invisible to a softcore that polls a
status level once per main-loop pass: the loop takes milliseconds per pass while decoding, so the pulse is caught about 1 % of the
time. A read of "vblank status" therefore looks like a dead wire. The reliable primitive is a free-running frame counter in the
CPU's clock domain (synchronise the vsync level with a plain multi-flop synchroniser, count rising edges, expose the count in the
upper half of the status register): firmware reads it twice and subtracts.

## Evidence

Polled level: 0 edges per second measured on the Pocket. Counter: about 60 frames per second on the same design, same measurement
window. The synchroniser feeding the counter is a single-bit level crossing (3 stages); the pulse is thousands of
destination clocks wide, so no multi-bit value crosses a clock domain.

## How to validate on hardware

Show the counter difference over one second on a diagnostic page and compare with the video timing (for example a 500 x 400 total frame at a 12 MHz pixel clock is 60 frames per second). Do it before building anything that schedules drawing around vblank.
