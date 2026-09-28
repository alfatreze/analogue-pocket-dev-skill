---
id: KB-067
title: A hardware feature can be fully built and gated correctly in RTL while firmware never loads its configuration data
status: docs-verified
confidence: medium
first_seen: 2026-09-28
last_verified: 2026-09-28
tags: [firmware,rtl,testing,config-load]
applies_to: any project splitting a hardware opcode/probe (self-test) path from a hardware
  configuration-load path (e.g. a small on-chip LUT/CLUT/coefficient table driven by MMIO writes)
sources:
  - a Cyclone V openFPGA core project (repository name withheld per this skill's own no-project-naming convention)
---

## Claim

A hardware draw/compute opcode can be built, RTL-simulated, Quartus-fitted, gated behind a correct
runtime "is this feature present" probe, and still produce visibly wrong output on real hardware for a
reason that has nothing to do with any of that: the opcode itself decodes and dispatches correctly, but
it reads a small on-chip lookup table (loaded via its own separate MMIO write path) that firmware simply
never writes. Every test that exists — opcode-decode simulation, the feature-presence probe, the
Quartus fit and timing closure — proves the datapath is wired correctly. None of them prove the
*configuration data* the datapath depends on was ever loaded, because "is the feature present" and "is
the feature correctly configured" are two different questions with two different failure surfaces, and
it is easy to write tests that only cover the first.

Concretely: a new opcode implementing rounded rectangles read its per-row corner-cut geometry from a
16-entry sticky lookup table loaded through its own dedicated pair of MMIO registers (index + data,
auto-incrementing), separate from the opcode-dispatch/command-FIFO path. The table's hardware reset
value was all-zero (i.e. "no cut" for every row) — a safe, fail-quiet default that never causes a hang
or a crash. The RTL was simulated and verified; a runtime probe correctly detected whether the opcode's
hardware existed at all; the software fallback path that draws the same shape without hardware was
exercised and correct. But the one function meant to call the table-load routine before every hardware
draw was never wired up in the actual call site, so on real hardware every hardware-drawn instance of
the shape silently degraded to a plain square — a real, user-visible regression versus the pure-software
path it was meant to accelerate, invisible to every test in the suite because none of them asked "was
the configuration table actually loaded for this draw," only "does the opcode decode and dispatch."

## Evidence

Found by a source-code review, not by a fresh hardware read: the table-load helper function existed,
was correctly implemented and host-tested in isolation, but grep/read of the one real call site
(the higher-level draw wrapper that is supposed to call it before issuing the hardware opcode) showed
it was never actually invoked there. The RTL comment describing the table's reset behavior ("resets to
all-zero, nothing loads it") was itself the tell once someone went looking, but nothing in the existing
automated test suite (RTL simulation, host-side firmware tests, or the runtime hardware-presence probe)
would have caught it, because all three only exercise "opcode present and decodes" or "table-load
function computes the right values when called," never "is the table-load function actually reached
from the real call site before a real draw." This specific instance's *fix* (wiring the missing call)
has not yet been independently confirmed against a fresh hardware photo as of this writing — the finding
itself (the call was missing) is a direct, unambiguous source-code fact, not an inference.

## How to validate on hardware

This is a general testing-discipline lesson, not a single hardware fact to reproduce. On any project with
a similar split (an opcode/feature-presence probe plus a separate configuration-load MMIO path — a CLUT,
a coefficient table, a palette, a calibration register set, anything with its own "is it stale / has it
been written this session" state): add a test, or at minimum a manual checklist item, that specifically
asks "was the configuration data for this draw/operation actually written before it was used," not just
"does the probe report the feature present" or "does the load function produce correct values when
called directly." A cheap version: instrument the real call site (not a synthetic harness) with a
counter or flag proving the load path was reached at least once before the first hardware use in a real
boot, and assert on it in a diagnostic build.
