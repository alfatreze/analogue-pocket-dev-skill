# Toolchain constraints: Quartus Prime editions and Cyclone V (validated 2026-09-23)

Read this before trusting any Quartus / Intel / Altera advice. Most documentation online is written for other editions or device families and silently does not apply to a Cyclone V core.

## Edition and device matrix (source-verified, KB-049)
| Edition | Cost | Cyclone V | Notes |
|---|---|---|---|
| **Lite** | free | yes (all versions 16.1 to 25.1) | Also Cyclone 10 LP, Cyclone IV, MAX 10/V/II. No Stratix, no Arria V/10. What the Pocket community uses (Lite 17.1 and 25.1 both reported working for the 5CEBA4F23C8). |
| **Standard** | paid license | yes | Adds Stratix IV/V, Arria II/V/10. Same compiler generation as Lite. |
| **Pro** | paid license | **no** | Agilex 7/5/3, Stratix 10, Arria 10, Cyclone 10 GX only. New compiler with different features. |
Common misstatement: "Cyclone V only works in Lite". Correct: Lite **or** Standard, never Pro. Re-check with `python3 scripts/refresh.py toolchain` (reads the distributor mirror of Altera's chart; Altera's own pages return 403).

## The documentation trap
- Anything titled or numbered as a **Pro Edition** guide (for example the Pro user guide 683641, "Guideline: Retarget or Balance DSP Blocks", Pro physical-synthesis / Hyper-Retiming chapters, Pro Rapid Recompile) describes a compiler that cannot target Cyclone V. Treat such advice as an idea to test, not a fact about your build.
- The relevant documents are the **Quartus Prime Standard Edition** handbook/user guide (for Lite too), the **Cyclone V Device Handbook** (memory blocks, DSP, PLL, I/O), and the Timing Analyzer chapters for the Standard series.
- Edition claims found on the web ("Lite lacks X") are often secondary or outdated. Only a report from your own edition settles it: `python3 scripts/refresh.py edition path/to/ap_core.fit.rpt` prints the edition string, the physical-synthesis options and the number of registers the fitter actually retimed.

## Edition-gating claims: distrust, then test
Rule: never accept "feature X is Standard-only / Pro-only" or "Lite lacks X" (or the reverse, "X works because the Pro guide lists it") without clear confirmation: the vendor's own text actually read for THIS edition and device, or a run on your own edition. When neither exists, say the claim is unconfirmed and **suggest a test**, and record it as community-reported.

Track record (2026-09-23), why the rule exists:
| Claim as found | Outcome |
|---|---|
| "Lite lacks register retiming" (Wikipedia, repeated by search summaries) | **Refuted** by a Lite 25.1 Cyclone V report: retiming On, 1,132 registers retimed (KB-050) |
| "Cyclone V only works in Lite" (working assumption) | **Partly wrong**: Standard also supports it; Pro does not (KB-049) |
| Rapid Recompile usable (cited Pro/Standard handbook) | **Unconfirmed**, one snippet says not in Lite; not tested (OQ-11) |
| DSP_BLOCK_BALANCING can force an adder off a DSP (cited a Pro guideline) | **Unconfirmed** for Cyclone V and for adders (KB-045, local) |
| "Auto Fit stops optimizing early, so switch to Standard Fit" | **Misapplied**: for builds failing timing Auto Fit already runs full effort (KB-048, local) |
| Cyclone V absent from Pro | **Confirmed** by the vendor's device-support table (device-support charts are reliable; feature-availability prose is not) |
Score: 1 confirmed, 1 refuted, 1 partly wrong, 3 unconfirmed or misapplied.

How to test cheaply, in order:
1. Your own reports: `python3 scripts/refresh.py edition path/to/ap_core.fit.rpt` (edition string, physical-synthesis options, retimed-register count).
2. A probe project: `python3 scripts/qsf_probe.py make DIR --assign '<qsf line>'`, compile with `quartus_sh --flow compile probe` on a machine with Quartus, then `qsf_probe.py check DIR`. Verdicts: REJECTED (Quartus prints an ignored/unsupported warning), ACCEPTED+APPLIED (the setting shows as non-default in Fitter Settings), ACCEPTED-NOT-SHOWN (inconclusive). Quote the exact lines and the version as evidence.
3. The GUI/quartus_sh help text of the installed edition (options that are absent or greyed out).
Record the verdict in the knowledge base with the edition and version. Entries tagged `edition-claim` cannot be docs-verified or source-verified without an `evidence:` line naming the report or test (`kb.py validate` enforces this).

## What has been checked
| Claim | Status | Evidence |
|---|---|---|
| Cyclone V in Standard and Lite, not Pro | source-verified (KB-049) | distributor chart tables + a community core's README |
| "Lite lacks register retiming" | disputed (KB-050) | a Lite 25.1 Cyclone V fit report shows retiming ON and 1,132 registers retimed; the claim traces to Wikipedia |
| "Lite lacks incremental compilation / design partitioning / partial reconfiguration" | community-reported | secondary sources only; not tested |
| Rapid Recompile available in Lite | community-reported, likely no | v18.0 comparison snippet says Pro and Standard only; confirm in the GUI |
| Auto Fit vs Standard Fit | disputed (local KB-048) | Intel message: no optimization skipped when timing needs full effort |

## Report fields worth knowing (Lite 25.1 fit report)
`Fitter Effort` (Auto Fit), `Physical Synthesis Effort Level` (Normal; higher levels are an untested lever, see open questions), `Perform Register Retiming / Duplication / Combinational Logic ... for Performance`, and the physical-synthesis netlist-change table (`Retimed Register`, `Modified`, `Deleted`).

## Fetching Intel/Altera material
`intel.com` and `altera.com` pages, `community.intel.com` and `community.altera.com` return HTTP 403 to curl and often to WebFetch. `docs.altera.com` is JavaScript-rendered (empty to curl). Usable: distributor and university mirrors (Macnica charts, course PDFs), Wikipedia, GitHub, and WebSearch result text (label snippet-only claims low confidence).
