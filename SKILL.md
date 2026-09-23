---
name: analogue-pocket-dev
description: "Analogue Pocket openFPGA/APF core development reference, Quartus Prime Lite/Standard and Cyclone V toolchain constraints (Cyclone V builds in Lite or Standard, never Pro), and an evidence-graded knowledge base from Analogue's developer docs, the open-fpga repos and community cores. Use for Pocket core work: core.json/data.json/interact.json/video.json/input.json, data slots and saves, BRIDGE bus and 0xF8000000 host/target commands (0180/0184/0188), boot sequence, Chip32, core_top.v/core_bridge_cmd.v, SDRAM/PSRAM/SRAM/cartridge/link hardware, video and I2S audio timing, .rbf_r, packaging, SD layout, JTAG/SignalTap. Also Quartus edition questions, Cyclone V (5CEBA4F23C8) timing closure, fitter and physical-synthesis settings, M10K/MLAB/DSP mapping, SDC constraints, build time; even when openFPGA is not mentioned."
---

# Analogue Pocket openFPGA development

Sources (all read in full): https://www.analogue.co/developer/docs/* (every page, incl. Chip32 subpages and changelogs) and https://github.com/open-fpga (core-template, four example cores, bass-chip32). Docs are versioned by framework version (1.1 → 2.3); when something looks version-dependent check `references/changelog.md`. Live docs can be curl'd (`curl -sL -A Mozilla/5.0 <url>`); WebFetch summaries drop detail and some pages 404 through it.

**First use:** `references/docs-snapshot/` (verbatim Analogue docs) and `references/repo-src/` (Analogue template RTL) are NOT stored in this repo because they belong to Analogue. If those folders are missing or empty, run `python3 scripts/bootstrap.py` once; it downloads them locally (git-ignored). Everything else here is self-contained.

## Where to look (read only what the task needs)
| Need | File |
|---|---|
| JSON files: every field, limit, bitmap, gotcha (core, data, interact, video, input, instance, variants) | `references/json-files.md` |
| BRIDGE commands, 0xF8xxxxxx map, handshake, structs, result codes, slot size table | `references/host-target-commands.md` |
| Boot/shutdown order | `references/docs-snapshot/core-boot-process.txt` (summary below) |
| Video/audio timing, pad/keyboard/mouse bits, RAM parts, cartridge/link/IR | `references/hardware-video-audio-input.md` |
| Chip32 VM (loader programs) | `references/chip32.md`, `references/repo-src/{example_chip32.asm,chip32.vm.arch}` |
| SD layout, packaging, rbf_r, icons, library images, palettes, debug tools | `references/sd-packaging-assets.md` |
| Which framework version added what | `references/changelog.md` |
| Real template/example RTL behavior (what is and isn't implemented) | `references/template-and-examples.md`, `references/repo-src/*.v` |
| Verbatim doc text for anything above | `references/docs-snapshot/*.txt` (local after bootstrap; grep it) |
| Quartus edition and Cyclone V constraints (Lite/Standard yes, Pro no), how to verify an edition claim, fetching Intel docs | `references/toolchain-constraints.md` |
| Community-learned, evidence-graded knowledge (saves/flush, CDC, timing, video, savestates...) | `references/knowledge-base/INDEX.md` then the entry file |
| Design patterns and workarounds seen in real cores | `references/knowledge-base/approaches.md` |
| Unknowns with a test plan | `references/knowledge-base/open-questions.md` |
| Where community knowledge lives and what could not be reached | `references/knowledge-base/resources.md` |

## Core mental model
- A core = bitstream (`.rbf_r`) + JSON definitions. You own the Primary Core FPGA; Analogue OS runs on a separate System FPGA and talks to your core over the APF BRIDGE bus. Host = Pocket, Target = your core; both can issue commands.
- Four buses: BRIDGE (32-bit peripheral, few MB/s, no arbitration, 0xF8xxxxxx reserved), PAD (controllers + heartbeat), VIDEO (RGB888, 16x16–800x720, own pixel clock), AUDIO (I2S 48 kHz 16-bit, MCLK 12.288 MHz).
- clk_74a and clk_74b are asynchronous to each other and to your PLL clocks; every crossing needs a synchronizer. `core_bridge_cmd` must be clocked directly from clk_74a.
- Data slots (≤32, 16-bit ids) carry assets/saves into bridge address space (`address`) or stay on the SD card (`deferload`) for target read/write.
- Start from `open-fpga/core-template`; do not edit `src/fpga/apf/`.

## Boot sequence (host view)
Bitstream loaded → core PLLs/FSM, status 1 *booting* → Pocket waits 100 ms and polls 0x0000 until 2 *setup* (RAM ready; no video/audio yet) → cartridge probe, host 00B1 → up to 32 bridge writes from variant+instance JSON → 0082 request write + data for each slot in order (core may watch/refuse) → 008F all complete → 0090 RTC → core sends target 0140 Ready-to-Run (status 3 *idle*) → persisted interact values written → cart power → 0011 Reset Exit, status 4 *running*.
Shutdown: 0010 Reset Enter → save interact persist → optional slot reload + 0011 → 0080 request read then read out nonvolatile slots (size from the 0x2000 table) → bitstream wiped. Heartbeat loss at any time makes Pocket reload the core.

## Practices that prevent the common failures
1. **Trust the source over the summary when they conflict; trust hardware over both.** Docs list commands (e.g. target 0188 flush, 0181/0185, 0152) that the shipped template FSM never issues; the template is a starting point, not a complete implementation. Read `references/template-and-examples.md` before assuming a command "just works".
2. **Bridge reads are asynchronous-ish.** Read data may arrive up to the next read strobe; write muxes/return paths so back-to-back reads cannot return stale or shifted data, and test back-to-back access explicitly.
3. **Persistence has three distinct paths:** nonvolatile data slots (written at shutdown from the size table), target write/flush commands on deferload slots, and interact.json `persist` values (`/Settings/Author.Core/Interact/interact_persist.json`, written when the core is quit). Say which one a test relies on; only quitting the core (not pulling the card) triggers APF writes.
4. **Change one `parameters` bit or one JSON field at a time.** The Pocket gives almost no feedback on malformed JSON; check Tools > Developer > Builds and enable Debug Logging (`/System/Logs/`).
5. **Rebuild ⇒ re-reverse.** Every Quartus rebuild needs a fresh `.rbf_r`; a stale one silently loads the old core. Compare SHA-256 of the file on the card with the build output.
6. **Bump `framework.version_required`** whenever using 2.x features (48-bit commands need 2.1) and keep `date_release`/`version` current for packaged releases.
7. **Use safe defaults for unused I/O** (copy the template tie-offs): mis-set cartridge translators with a powered cart can destroy cart data; PSRAM chip enables must never both assert; IR TX only PWM.
8. **Distrust edition-gating claims; test them.** Cyclone V builds only in Quartus Prime Lite or Standard, never Pro (KB-049), but claims like "X is Standard-only / Pro-only", "Lite lacks X" or "the Pro guide says X works" are unreliable: of the ones checked so far one was refuted by a real Lite report (retiming, KB-050), others cited Pro documents or could not be confirmed. Without clear confirmation (vendor text read for this edition and device, or a run on your own edition), call the claim unconfirmed and suggest a test: `scripts/refresh.py edition <ap_core.fit.rpt>` or a probe project via `scripts/qsf_probe.py make/check`. See `references/toolchain-constraints.md`. Tag such KB entries `edition-claim`; state edition, version and device family in `applies_to`.
9. **Record results.** If your project keeps an audit trail or log, record each hardware result (what changed, what was observed, firmware version) so failed hypotheses are not repeated.

## Known doc inconsistencies (don't be misled)
- core.json sample has `"/"` where `shortname` belongs.
- variants.json text says `data_id_to/from`, sample uses `data_id/data_id_override`; variants are "upcoming" and instance JSON superseded variant selection.
- Boot doc mentions `[0182 Data slot copy]`, absent from the command list.
- Overview says video scaler customization is "upcoming" though video.json scaler modes work (2.x).
- audio.json is a stub (`magic` only).

## Evolving knowledge base (how this skill keeps learning without being polluted)
**Concurrency rule:** other agents and the weekly refresh write to the KB concurrently; re-list entries immediately before editing and never edit an entry you did not create in this session. (The one sanctioned exception is `kb.py promote`/`note` on an existing id, which re-verifies the target with `--title-contains`, backs it up first, and never rewrites claims.)

Entries live in `references/knowledge-base/entries/KB-NNN-*.md`; `INDEX.md` is generated. Every claim carries a status: **hardware-validated** (our own Pocket test, evidence names the test id) > **source-verified** (real RTL/code in >=2 places, or docs+code) > **docs-verified** > **community-reported** (one third-party claim) ; plus **disputed** and **refuted** (both kept, never deleted).

Rules when answering: consult the index for the topic; cite the entry id and status when you rely on one; present `community-reported`/`disputed` as leads to test, never as facts; prefer suggesting the entry's "How to validate" test over acting on the claim.

Rules when learning something new (from a hardware result, a source read, a forum/issue thread a person pastes, an upstream doc change):
1. Check `INDEX.md` for an existing entry; update rather than duplicate.
2. New claim: `python3 scripts/kb.py new "title" --tags a,b --source URL` (starts as community-reported, low confidence). It prints the allocated id AND file path: edit only that returned path, and never assume the next free id (ids are claimed atomically, but another session may create entries at any moment). Fill Claim / Evidence / How to validate on hardware, quoting the source exactly and stating scope (firmware version, core, date). If a claim came from a search summary you did not open, say so and keep confidence low.
3. Promote only with evidence: `kb.py promote KB-007 --to hardware-validated --evidence "T-12: <what was observed on hardware>" --title-contains "<words from that entry's title>"` (refuses if the title does not match, so a stale or wrong id cannot be promoted; the entry is copied to git-ignored `local/backups/` first) after an actual Pocket run (name your test/audit id). `source-verified` needs a second independent source or a matching official doc. A failed test uses `--to refuted`. Conflicting credible sources: `--to disputed`.
4. `kb.py validate` must pass and `kb.py index` regenerate before finishing. `kb.py stale` lists unvalidated community claims older than 30 days: propose a test for them.
5. Never edit the SKILL.md core sections to state an unvalidated claim; only validated entries may change guidance there. **Claims are immutable once committed:** to correct or extend knowledge, add evidence to the entry (append only), create a new entry, or change status with `kb.py promote` (refuted/disputed). `kb.py validate` enforces this against git HEAD (plus a leak guard that rejects project-private text in publishable files; put project names in git-ignored `references/knowledge-base/local/private-patterns.txt`). `kb.py install-hook` blocks commits that fail it. Fix a genuine typo with `kb.py validate --allow-claim-edit KB-nnn`.
6. Drift check (run at the start of a Pocket work session or on a schedule): `python3 scripts/refresh.py docs` (exit 2 = changed/new/gone pages; add `--update` after reading the diff to refresh `docs-snapshot/`) and `python3 scripts/refresh.py repos` (watched community repos; `--update` records new HEADs). Reports only: read what changed, then add or adjust entries and `references/changelog.md`; do not auto-rewrite claims.
7. Project-private material stays local: use `kb.py new --local` for entries drawn from your own project's results and `kb.py note KB-001 "text"` for how a public entry applies to your project. Those live in git-ignored `local-entries/` and `local/`; `INDEX.local.md` lists everything, `INDEX.md` only public entries. Read both indexes when they exist. Log updates in your project's own log.
8. To publish accumulated changes: `python3 scripts/release.py` (validates, shows the diff, asks before commit and push, rebuilds the .skill from committed files). Only run it when the human asks; the weekly refresh leaves changes uncommitted on purpose.
