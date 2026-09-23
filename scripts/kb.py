#!/usr/bin/env python3
"""Knowledge-base tool for the analogue-pocket-dev skill (stdlib only).

  kb.py validate [--allow-claim-edit KB-nnn]  lint entries + guards: no project-private text in publishable files,
                                 no rewritten claims / truncated evidence vs git HEAD (exit 1 on problems)
  kb.py install-hook             pre-commit hook that runs validate
  kb.py index                    regenerate references/knowledge-base/INDEX.md
  kb.py new "title" [--tags a,b] [--source URL ...] [--local]  create a community-reported entry (--local = git-ignored, project-private)
  kb.py note KB-001 "text"     add a project-specific relevance note (git-ignored)
  kb.py promote KB-001 --to STATUS --evidence "text" --title-contains "words in title"
                                 change status (refuses if the title does not match; backs up the entry first)
  kb.py stale [--days N]         entries needing (re)verification
  kb.py show KB-001

Status ladder (never skip evidence):
  community-reported  one third-party claim, not checked by us
  docs-verified       stated in official Analogue docs (cite page)
  source-verified     confirmed by reading real RTL/code in >=2 independent places, or docs+code
  hardware-validated  reproduced on a Pocket by our own test (evidence must name the test id)
  refuted             a test or source contradicts it (kept, never deleted)
  disputed            credible sources conflict (kept until resolved)
"""
import argparse, datetime, os, re, shutil, subprocess, sys

ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), ".."))
KB = os.path.join(ROOT, "references", "knowledge-base")
ENT = os.path.join(KB, "entries")
LOC = os.path.join(KB, "local-entries")   # git-ignored, project-private entries
NOTES = os.path.join(KB, "local", "relevance.md")  # git-ignored project relevance notes
STATUSES = ["community-reported", "docs-verified", "source-verified",
            "hardware-validated", "refuted", "disputed"]
CONF = ["low", "medium", "high"]
REQ = ["id", "title", "status", "confidence", "first_seen", "last_verified", "tags", "sources"]
TODAY = datetime.date.today().isoformat()


def parse(path):
    txt = open(path, encoding="utf-8").read()
    m = re.match(r"---\n(.*?)\n---\n?(.*)", txt, re.S)
    if not m:
        raise ValueError("missing frontmatter")
    meta, key = {}, None
    for line in m.group(1).split("\n"):
        if re.match(r"^\s+- ", line) and key:
            meta[key].append(line.strip()[2:].strip())
        else:
            k, _, v = line.partition(":")
            key, v = k.strip(), v.strip()
            if v.startswith("[") and v.endswith("]"):
                meta[key] = [x.strip() for x in v[1:-1].split(",") if x.strip()]
            elif v == "":
                meta[key] = []
            else:
                meta[key] = v.strip('"')
    return meta, m.group(2), txt


def entries():
    out = []
    for d in (ENT, LOC):
        if not os.path.isdir(d):
            continue
        for f in sorted(os.listdir(d)):
            if f.endswith(".md"):
                p = os.path.join(d, f)
                meta, body, raw = parse(p)
                out.append((p, meta, body, raw))
    return out


# ---------------------------------------------------------------- guards ----
# Public files must stay general and existing claims must not be rewritten.
DEFAULT_PRIVATE = [r"\bA-\d{3}\b", r"AUDIT_TRAIL", r"/Users/", r"docs/vendor", r"CURRENT_STATUS"]
PRIVATE_FILE = os.path.join(KB, "local", "private-patterns.txt")  # git-ignored; add project names here


def git(*args):
    r = subprocess.run(["git", "-C", ROOT, *args], capture_output=True, text=True)
    return r.stdout if r.returncode == 0 else None


def private_patterns():
    pats = list(DEFAULT_PRIVATE)
    if os.path.exists(PRIVATE_FILE):
        pats += [l.strip() for l in open(PRIVATE_FILE) if l.strip() and not l.startswith("#")]
    return [re.compile(x, re.I if i >= len(DEFAULT_PRIVATE) else 0) for i, x in enumerate(pats)]


def publishable_files():
    """Files that would be published: tracked + untracked-but-not-ignored (md/json, excluding scripts)."""
    out = git("ls-files", "--cached", "--others", "--exclude-standard")
    if out is None:
        return None
    return [f for f in out.split("\n") if f.endswith((".md", ".json")) and not f.startswith("scripts/")
            and f not in ("LICENSE", "NOTICE.md")]


def leak_guard(errs):
    files = publishable_files()
    if files is None:
        print("note: not a git checkout, leak guard skipped"); return
    pats = private_patterns()
    for f in files:
        path = os.path.join(ROOT, f)
        if not os.path.exists(path):
            continue
        for n, line in enumerate(open(path, encoding="utf-8", errors="ignore"), 1):
            for pat in pats:
                if pat.search(line):
                    errs.append(f"LEAK {f}:{n} matches /{pat.pattern}/ (project-private text in a publishable file; "
                                f"use `kb.py new --local` or `kb.py note`)")
                    break


def section(body, name):
    m = re.search(rf"## {name}\n(.*?)(?=\n## |\Z)", body, re.S)
    return m.group(1).strip() if m else ""


def immutable_guard(errs, allow):
    """A published claim must not be rewritten. Evidence may grow but not lose text."""
    top = git("rev-parse", "--show-toplevel")
    if top is None:
        return
    top = top.strip()
    for p, m, body, _ in entries():
        if os.path.dirname(p) != ENT or m["id"] in allow:
            continue
        old = git("show", "HEAD:" + os.path.relpath(p, top))
        if old is None:
            continue  # new, uncommitted entry
        try:
            om = re.match(r"---\n(.*?)\n---\n?(.*)", old, re.S)
            obody = om.group(2)
        except AttributeError:
            continue
        if section(body, "Claim") != section(obody, "Claim"):
            errs.append(f"{m['id']}: '## Claim' differs from the committed version. Claims are never rewritten: create a new "
                        f"entry and mark this one refuted/disputed (kb.py promote), or pass --allow-claim-edit {m['id']} for a typo fix")
        if section(obody, "Evidence") and section(obody, "Evidence") not in section(body, "Evidence"):
            errs.append(f"{m['id']}: '## Evidence' lost committed text (evidence may only be appended)")
        if m["id"] not in allow:
            ostat = re.search(r"^status: (.*)$", om.group(1), re.M)
            if ostat and ostat.group(1) != m["status"] and m["status"] == "hardware-validated" and not m.get("evidence"):
                errs.append(f"{m['id']}: promoted to hardware-validated without evidence")


def validate(allow=()):
    errs, ids = [], set()
    for p, m, body, _ in entries():
        n = os.path.basename(p)
        for k in REQ:
            if k not in m or m[k] in ("", []):
                errs.append(f"{n}: missing '{k}'")
        if m.get("status") not in STATUSES:
            errs.append(f"{n}: bad status {m.get('status')!r}")
        if m.get("confidence") not in CONF:
            errs.append(f"{n}: bad confidence {m.get('confidence')!r}")
        for d in ("first_seen", "last_verified"):
            if not re.match(r"^\d{4}-\d{2}-\d{2}$", str(m.get(d, ""))):
                errs.append(f"{n}: {d} must be YYYY-MM-DD")
        if m.get("id") in ids:
            errs.append(f"{n}: duplicate id")
        ids.add(m.get("id"))
        if not n.startswith(str(m.get("id", "?")) + "-"):
            errs.append(f"{n}: filename must start with its id")
        st = m.get("status")
        if st == "hardware-validated" and not m.get("evidence"):
            errs.append(f"{n}: hardware-validated needs 'evidence:' naming the test/audit id")
        if st == "source-verified" and len(m.get("sources", [])) < 2:
            errs.append(f"{n}: source-verified needs >=2 sources")
        if "edition-claim" in [t.lower() for t in m.get("tags", [])] and st in ("docs-verified", "source-verified") and not m.get("evidence"):
            errs.append(f"{n}: edition-claim entries need an 'evidence:' line naming the report/test/primary page before they can be {st} (test it: scripts/qsf_probe.py or refresh.py edition)")
        if st == "refuted" and not m.get("evidence"):
            errs.append(f"{n}: refuted needs 'evidence:'")
        for s in ("## Claim", "## Evidence", "## How to validate"):
            if s not in body:
                errs.append(f"{n}: missing section '{s}'")
    TOOL = {"quartus", "fitter", "dsp", "m10k", "mlab", "sdc", "toolchain", "cyclone-v", "signaltap", "synthesis"}
    for p_, m_, *_ in entries():
        if TOOL & {t.lower() for t in m_.get("tags", [])} and not re.search(r"lite|standard|pro\b|edition|quartus", str(m_.get("applies_to", "")), re.I):
            print(f"WARN {os.path.basename(p_)}: toolchain entry without edition/version in applies_to (say Lite/Standard/Pro and the Quartus version)")
    leak_guard(errs)
    immutable_guard(errs, set(allow))
    for e in errs:
        print("ERROR", e)
    print(f"{len(ids)} entries, {len(errs)} problems")
    return 1 if errs else 0


def index():
    write_index(False)
    if os.path.isdir(LOC):
        write_index(True)


def write_index(include_local):
    rows = [r for r in entries() if include_local or os.path.dirname(r[0]) == ENT]
    order = {s: i for i, s in enumerate(["hardware-validated", "source-verified", "docs-verified",
                                         "disputed", "community-reported", "refuted"])}
    rows.sort(key=lambda r: (order.get(r[1]["status"], 9), r[1]["id"]))
    lines = ["# Knowledge base index (generated by scripts/kb.py index; do not edit)\n",
             "Trust order: hardware-validated > source-verified > docs-verified > community-reported. "
             "Cite the entry id and status whenever you rely on one; never present community-reported as fact.\n",
             "| id | status | conf | last verified | title | tags |", "|---|---|---|---|---|---|"]
    if include_local:
        lines[0] = "# Knowledge base index INCLUDING local project entries (git-ignored; generated)\n"
    for p, m, *_ in rows:
        d = "entries" if os.path.dirname(p) == ENT else "local-entries"
        lines.append(f"| [{m['id']}]({d}/{os.path.basename(p)}) | {m['status']} | {m['confidence']} | "
                     f"{m['last_verified']} | {m['title']} | {', '.join(m['tags'])} |")
    name = "INDEX.local.md" if include_local else "INDEX.md"
    open(os.path.join(KB, name), "w").write("\n".join(lines) + "\n")
    print("wrote", name + ",", len(rows), "entries")


def slug(t):
    return re.sub(r"[^a-z0-9]+", "-", t.lower()).strip("-")[:50]


def new(a):
    i = claim_id()
    ent = LOC if a.local else ENT
    os.makedirs(ent, exist_ok=True)
    src = "".join(f"  - {s}\n" for s in (a.source or ["TODO: add source"]))
    body = (f"---\nid: {i}\ntitle: {a.title}\nstatus: community-reported\nconfidence: low\n"
            f"first_seen: {TODAY}\nlast_verified: {TODAY}\ntags: [{a.tags or ''}]\n"
            f"applies_to: unknown\nsources:\n{src}---\n\n## Claim\n\n## Evidence\n\n"
            f"## How to validate on hardware\n")
    p = os.path.join(ent, f"{i}-{slug(a.title)}.md")
    open(p, "x").write(body)
    print(f"created {i}  path: {p}")
    print("edit ONLY this path; never assume the next free id (other sessions and the weekly refresh write here too)")


def backup(path):
    """Copy an existing entry to local/backups/ (git-ignored) before any write."""
    d = os.path.join(KB, "local", "backups")
    os.makedirs(d, exist_ok=True)
    dst = os.path.join(d, datetime.datetime.now().strftime("%Y%m%d-%H%M%S-") + os.path.basename(path))
    shutil.copy2(path, dst)
    return dst


def claim_id():
    """Allocate the next free id atomically. A marker file created with O_EXCL means two sessions
    running `new` at the same time can never get the same id (unlike 'max existing id + 1')."""
    cd = os.path.join(KB, "local", "claims")
    os.makedirs(cd, exist_ok=True)
    n = max([int(m["id"].split("-")[1]) for _, m, *_ in entries()] or [0]) + 1
    while True:
        i = "KB-%03d" % n
        try:
            os.close(os.open(os.path.join(cd, i), os.O_CREAT | os.O_EXCL | os.O_WRONLY))
            return i
        except FileExistsError:
            n += 1


def find(i):
    for p, m, body, raw in entries():
        if m["id"] == i:
            return p, m, body, raw
    sys.exit(f"no such entry {i}")


def promote(a):
    if a.to not in STATUSES:
        sys.exit(f"status must be one of {STATUSES}")
    p, m, body, raw = find(a.id)
    if a.title_contains.lower() not in m["title"].lower():
        sys.exit(f"REFUSED: {a.id} is titled {m['title']!r}, which does not contain {a.title_contains!r}. "
                 "Re-list entries (kb.py index) and confirm the id; entries can be created concurrently by other sessions.")
    bk = backup(p)
    old = m["status"]
    raw = re.sub(r"^status: .*$", f"status: {a.to}", raw, count=1, flags=re.M)
    raw = re.sub(r"^last_verified: .*$", f"last_verified: {TODAY}", raw, count=1, flags=re.M)
    raw = re.sub(r"^evidence: .*\n", "", raw, flags=re.M)
    raw = raw.replace("\nsources:", f"\nevidence: {a.evidence}\nsources:", 1)
    open(p, "w").write(raw)
    os.makedirs(os.path.join(KB, "local"), exist_ok=True)
    with open(os.path.join(KB, "local", "LOG.md"), "a") as f:
        f.write(f"- {TODAY} {a.id} ({m['title'][:60]}): {old} -> {a.to}. {a.evidence} [backup: {os.path.basename(bk)}]\n")
    print(f"{a.id}: {old} -> {a.to}  (backup: {bk})")
    if validate() == 0:
        index()


def stale(a):
    cutoff = datetime.date.today() - datetime.timedelta(days=a.days)
    for p, m, *_ in entries():
        lv = datetime.date.fromisoformat(m["last_verified"])
        if m["status"] == "community-reported" and (datetime.date.today() - lv).days > 30:
            print(f"{m['id']} community-reported, unvalidated for {(datetime.date.today()-lv).days}d: {m['title']}")
        elif lv < cutoff and m["status"] not in ("refuted",):
            print(f"{m['id']} {m['status']}, last verified {lv}: {m['title']}")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sp = ap.add_subparsers(dest="cmd", required=True)
    v = sp.add_parser("validate"); v.add_argument("--allow-claim-edit", action="append", default=[], help="entry id whose claim may differ from HEAD (typo fix)")
    sp.add_parser("index"); sp.add_parser("install-hook", help="block commits that fail validate")
    n = sp.add_parser("new"); n.add_argument("title"); n.add_argument("--tags"); n.add_argument("--source", action="append"); n.add_argument("--local", action="store_true", help="project-private entry (git-ignored)")
    nt = sp.add_parser("note", help="append a project-specific relevance note (git-ignored)"); nt.add_argument("id"); nt.add_argument("text")
    pr = sp.add_parser("promote"); pr.add_argument("id"); pr.add_argument("--to", required=True); pr.add_argument("--evidence", required=True)
    pr.add_argument("--title-contains", required=True, help="text the entry title must contain; guards against a stale or wrong id")
    st = sp.add_parser("stale"); st.add_argument("--days", type=int, default=180)
    sh = sp.add_parser("show"); sh.add_argument("id")
    a = ap.parse_args()
    if a.cmd == "validate": sys.exit(validate(a.allow_claim_edit))
    elif a.cmd == "install-hook":
        hp = git("rev-parse", "--git-path", "hooks/pre-commit")
        hp = os.path.join(ROOT, hp.strip()) if hp else None
        if not hp: sys.exit("not a git checkout")
        open(hp, "w").write("#!/bin/sh\ncd \"$(git rev-parse --show-toplevel)\" && python3 scripts/kb.py validate\n")
        os.chmod(hp, 0o755); print("installed", hp)
    elif a.cmd == "index": index()
    elif a.cmd == "new": new(a)
    elif a.cmd == "promote": promote(a)
    elif a.cmd == "stale": stale(a)
    elif a.cmd == "show":
        print(find(a.id)[3])
        if os.path.exists(NOTES):
            m = re.search(rf"## {a.id}\n(.*?)(?=\n## KB-|\Z)", open(NOTES).read(), re.S)
            if m: print("\n[local relevance]\n" + m.group(1).strip())
    elif a.cmd == "note":
        find(a.id); os.makedirs(os.path.dirname(NOTES), exist_ok=True)
        open(NOTES, "a").write(f"\n## {a.id}\n{a.text}\n")
        print("noted", a.id)


if __name__ == "__main__":
    main()
