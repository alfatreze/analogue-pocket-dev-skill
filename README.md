# analogue-pocket-dev-skill

A [Claude Code](https://claude.com/claude-code) skill for **Analogue Pocket openFPGA / APF core development**: distilled reference for the core JSON files, data slots, the BRIDGE bus and host/target commands, boot flow, Chip32, hardware, video/audio timing and packaging, plus an **evidence-graded knowledge base** of community-learned behavior (saves and flush, size table, CDC, timing/seeds, savestates, ...) that grows over time.

Unofficial. See [NOTICE.md](NOTICE.md): Analogue's docs and APF code are not included.

## Install
```bash
git clone https://github.com/alfatreze/analogue-pocket-dev-skill ~/.claude/skills/analogue-pocket-dev
python3 ~/.claude/skills/analogue-pocket-dev/scripts/bootstrap.py   # fetch Analogue docs locally (git-ignored)
```
Then in Claude Code the skill loads automatically for Pocket/openFPGA work, or run `/analogue-pocket-dev`.
Claude.ai: zip the folder and upload under Settings > Skills.

## Layout
- `SKILL.md`: router, mental model, boot sequence, practices, and the rules for evolving the knowledge base
- `references/*.md`: JSON files, commands, hardware/video/audio, Chip32, SD/packaging, changelog, template internals
- `references/knowledge-base/`: `INDEX.md`, `entries/KB-*.md` (status: community-reported, docs-verified, source-verified, hardware-validated, disputed, refuted), `approaches.md`, `open-questions.md`, `resources.md`, `sources.json`
- `scripts/kb.py`: validate / index / new / note / promote / stale. `scripts/refresh.py`: detect doc and repo drift. `scripts/bootstrap.py`: fetch third-party material locally

## How knowledge is graded
A claim starts `community-reported`. It becomes `source-verified` only with two independent sources (or docs plus code) and `hardware-validated` only with a recorded Pocket test. Contradicted claims are kept as `refuted`/`disputed`. The skill instructs Claude to treat unvalidated claims as leads to test, never facts.

## Private, project-specific knowledge
Results from your own project go in git-ignored `references/knowledge-base/local-entries/` (`kb.py new --local`) and `local/` (`kb.py note`), so the public repo stays general.

## Guards
`kb.py validate` (also run by the pre-commit hook: `python3 scripts/kb.py install-hook`) fails when a committed claim is rewritten, evidence loses text, or project-private text (audit-trail ids (a letter, hyphen and three digits), local paths, plus names listed in your git-ignored `references/knowledge-base/local/private-patterns.txt`) appears in a publishable file.

## Contributing
Add entries with `python3 scripts/kb.py new ...`, then `kb.py validate` and `kb.py index`. Include exact source links, scope (firmware/core/date) and a hardware validation test.
