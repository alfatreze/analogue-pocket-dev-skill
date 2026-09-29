---
id: KB-073
title: Cyclone V MLAB is simple dual-port only (32x20, 640 bits per MLAB) and does not support mixed-width ports
status: docs-verified
confidence: high
first_seen: 2026-09-29
last_verified: 2026-09-29
tags: [quartus,cyclone-v,memory,mlab,inference]
applies_to: Cyclone V (incl. 5CEBA4F23C8) device architecture; applies to any Quartus edition that targets it (Lite, Standard). Handbook CV-52001/CV-52002, revision 2016.06.10
sources:
  - https://courses.cs.washington.edu/courses/cse371/references/Cyclone_V_Device_Handbook_Vol_1.pdf
---

## Claim

A Cyclone V MLAB is a 32-word x 20-bit **simple dual-port** RAM (one write port, one read port): ten ALMs,
each a 32 x 2 block, for 640 bits per MLAB. MLABs do not support mixed-width port configurations (those
exist only for M10K). Unregistered ROM address lines are allowed on MLAB only in the simple dual-port
mode. So a small RAM that needs two independent read addresses, or an M10K-style mixed-width port, cannot
map onto one MLAB as written. Quartus then has to duplicate the memory (one copy per read port, both
written from the same port), use M10K, or build it from registers.

This is a device-architecture fact. How Quartus reacts in each case (duplicate, move to M10K, or fall
back to ALM registers) is inference behaviour: it is not stated here and must be read from your own
map/fit report.

## Evidence

Cyclone V Device Handbook Volume 1 (2016.06.10, read via a university course mirror; the text was pulled
from the PDF streams, so no page numbers). Quotes: "Each MLAB supports a maximum of 640 bits of simple
dual-port SRAM", "you can configure these ALMs as ten 32 x 2 blocks, giving you one 32 x 20 simple
dual-port SRAM block per MLAB", "MLABs do not support mixed-width port configurations". A search summary
also said "MLAB does not support true dual-port RAM"; that matches the above, but the wording was not
found verbatim in the extracted text.

## How to validate on hardware

On a build: in the Analysis & Synthesis "RAM Summary" and the fitter resource section, check the block
type (MLAB / M10K / none) and the port mode reported for each inferred memory. A small RAM that shows up
as thousands of registers, or as M10K when you asked for `ramstyle = "MLAB"`, usually has a second read
address or a second write site. The usual fix is one write port with an explicit copy per read port,
each copy inferred on its own. Confirm with a synthesis-only run before spending a full fit.
