---
id: KB-058
title: A ternary read across two different multi-array concatenations breaks Quartus RAM inference, even with power-of-two sizes
status: community-reported
confidence: medium
first_seen: 2026-09-25
last_verified: 2026-09-25
tags: [quartus,cyclone-v,memory,m10k,inference]
applies_to: Quartus Prime Lite 25.1std, Cyclone V (5CEBA4)
sources:
  - a Cyclone V openFPGA core project (repository name withheld per this skill's own no-project-naming convention)
---

## Claim

Splitting one large RAM array into two smaller power-of-two-sized regions (a common workaround when the
total word count is not itself a power of two) can silently fail Quartus's RAM-inference pattern-matcher,
even though every region declared is individually a clean, ordinary power-of-two byte array. The specific
failing shape: reading the result via a ternary that selects between TWO DIFFERENT multi-array
concatenations in one statement, e.g. `rdata <= sel ? {b3[addr],b2[addr],b1[addr],b0[addr]} : {a3[addr],
a2[addr],a1[addr],a0[addr]};`. Every array involved reports "uninferred due to asynchronous read logic" and
the whole memory falls back to registers ("Cannot convert all sets of registers into RAM megafunctions"),
even though each individual array, read alone, infers cleanly. Local address wires, a module-port boundary,
and a `generate` block were each tested and ruled out as independent causes on the same design (isolating
experiments, not assumption) — the failure is specifically tied to the ternary-of-two-concatenations read
shape, not to splitting the memory itself, nor to any of the more commonly-suspected causes.

## Evidence

Confirmed on real Quartus `quartus_map` runs (synthesis-only, not just simulation) on a Cyclone V 5CEBA4
target, Quartus Prime Lite 25.1std. A 49,152-word (192 KB) region split into 32,768 + 16,384 word regions,
each their own clean power-of-two byte array (4 lanes each, `a0..a3`/`b0..b3`), failed with
`Error (276003): Cannot convert all sets of registers into RAM megafunctions`, and every one of the 8 arrays
individually reported `RAM logic ... is uninferred due to asynchronous read logic`. Three isolating
experiments were run to rule out the obvious suspects before finding the real cause: (1) removing a local
`idx` address wire between the port and the array reference — failed identically; (2) a plain single-array
module with no split/generate at all, proving module extraction is not the cause — synthesized cleanly,
"0 errors"; (3) the same split written inline in the parent module with no module boundary and no `generate`
block at all — failed identically, ruling out both suspects simultaneously. The one property every failing
version shared, and the one thing every OTHER successfully-inferred RAM in the same codebase (including the
original single-region array before the split) did NOT do: read via a ternary selecting between two
different multi-array concatenations, rather than a single, unconditional, directly-addressed
`reg <= array[addr];`.

**Fix confirmed working**: give each region its own plain, unconditional, directly-addressed registered read
into fresh per-region registers (one register per byte lane per region), then mux the ALREADY-REGISTERED
byte values together afterward in a separate combinational block, outside the clocked block that does the
reads. By the time the mux runs, nothing being selected between is an array reference any more, so it
carries no RAM-inference weight at all. Writes were also flattened from a nested if/else to one flat
single-condition statement per array lane, for the same "match the simple per-array template" reasoning,
though this was not independently isolated as necessary. Re-run with this fix: all 8 arrays inferred
cleanly as correctly-sized `altsyncram` megafunctions, "0 errors, 315 warnings", and the region sizes
(`NUMWORDS_A`/`NUMWORDS_B` in the synthesis log) matched the declared sizes exactly.

## How to validate on hardware

Not hardware validation in the traditional sense — this is a synthesis-stage (`quartus_map`) finding,
confirmed via the Analysis & Synthesis report's own RAM inference messages, not a Fitter or real-silicon
result. To reproduce: declare two or more same-shaped byte-lane arrays, read them through a ternary
selecting between two different multi-array concatenations, and check the synthesis log for "uninferred due
to asynchronous read logic" against each array individually. To confirm the fix generalizes beyond this one
project: try the same pattern (ternary-of-two-concatenations vs. register-then-mux) on a different Quartus
version/edition and record whether the same failure reproduces, since this has only been confirmed on
25.1std Lite so far.
