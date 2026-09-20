#!/usr/bin/env python3
"""Detect upstream drift so the skill can evolve (stdlib + curl + git).

  refresh.py docs            re-fetch analogue.co developer docs, report changed / new / vanished pages
  refresh.py docs --update   ...and overwrite references/docs-snapshot with the fresh text
  refresh.py repos           compare watched GitHub repos' HEAD against sources.json, report new commits
  refresh.py repos --update  record the new HEADs
Exit code 0 = nothing changed, 2 = changes found (so it can gate a scheduled task).
Changes are only REPORTS: read the diff, then add/adjust knowledge-base entries; never auto-edit claims.
"""
import argparse, difflib, hashlib, html, json, os, re, subprocess, sys

ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), ".."))
SNAP = os.path.join(ROOT, "references", "docs-snapshot")
SRC = os.path.join(ROOT, "references", "knowledge-base", "sources.json")
BASE = "https://www.analogue.co"
UA = ["-A", "Mozilla/5.0"]


def fetch(url):
    r = subprocess.run(["curl", "-sL", "-m", "40", *UA, "-w", "\n%{http_code}", url], capture_output=True, text=True)
    body, _, code = r.stdout.rpartition("\n")
    return code, body


def extract(raw):
    m = re.search(r"<main.*?</main>|<article.*?</article>", raw, flags=re.S)
    t = m.group(0) if m else raw
    t = re.sub(r"<(script|style|nav)[^>]*>.*?</\1>", "", t, flags=re.S)
    t = re.sub(r"<pre[^>]*>", "\n```\n", t).replace("</pre>", "\n```\n")
    t = re.sub(r"<tr[^>]*>", "\n| ", t)
    t = re.sub(r"</t[hd]>", " | ", t)
    t = re.sub(r"<li[^>]*>", "\n- ", t)
    t = re.sub(r"<h(\d)[^>]*>", lambda m: "\n" + "#" * int(m.group(1)) + " ", t)
    t = re.sub(r"<(p|div|br)[^>]*>", "\n", t)
    t = re.sub(r"<[^>]+>", "", t)
    return html.unescape(re.sub(r"\n\s*\n+", "\n", t))


def slug_of(name):
    n = name[:-4]
    return "/developer/docs" if n == "overview" else "/developer/docs/" + n.replace("__", "/")


def docs(update):
    if not os.path.isdir(SNAP) or not os.listdir(SNAP):
        print("docs-snapshot is empty: run `python3 scripts/bootstrap.py` first"); return False
    known = {f for f in os.listdir(SNAP) if f.endswith(".txt")}
    changed, gone, new_links = [], [], set()
    for f in sorted(known):
        path = "/developer/docs/overview" if f == "overview.txt" else slug_of(f)
        code, raw = fetch(BASE + path)
        if code != "200":
            gone.append(f"{f} (HTTP {code})"); continue
        new_links |= set(re.findall(r'href="(/developer/docs/[^"#?]*)"', raw))
        fresh = extract(raw)
        old = open(os.path.join(SNAP, f), encoding="utf-8").read()
        if hashlib.sha256(fresh.encode()).hexdigest() != hashlib.sha256(old.encode()).hexdigest():
            d = "\n".join(list(difflib.unified_diff(old.splitlines(), fresh.splitlines(), lineterm="", n=0))[:60])
            changed.append((f, d))
            if update:
                open(os.path.join(SNAP, f), "w", encoding="utf-8").write(fresh)
    have = {"/developer/docs/overview" if f == "overview.txt" else slug_of(f) for f in known} | {"/developer/docs", "/developer/docs/changelog"}
    unseen = sorted(new_links - have)
    for f, d in changed:
        print(f"CHANGED {f}\n{d}\n")
    for g in gone: print("GONE   ", g)
    for u in unseen: print("NEW PAGE", u, "(not in snapshot; fetch it and add to references/docs-snapshot)")
    print(f"docs: {len(changed)} changed, {len(gone)} gone, {len(unseen)} new" + (" (snapshot updated)" if update and changed else ""))
    return bool(changed or gone or unseen)


def repos(update):
    data = json.load(open(SRC))
    dirty = False
    for r in data["repos"]:
        out = subprocess.run(["git", "ls-remote", r["url"], "HEAD"], capture_output=True, text=True).stdout.split()
        head = out[0] if out else None
        if head is None:
            print("UNREACHABLE", r["url"]); continue
        if head != r.get("head"):
            dirty = True
            print(f"MOVED {r['url']}  {r.get('head','(none)')[:8]} -> {head[:8]}  ({r.get('why','')})")
            if update: r["head"] = head
    if update:
        json.dump(data, open(SRC, "w"), indent=2); print("sources.json updated")
    print("repos: " + ("changes found" if dirty else "no movement"))
    return dirty


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("what", choices=["docs", "repos"]); ap.add_argument("--update", action="store_true")
    a = ap.parse_args()
    sys.exit(2 if (docs if a.what == "docs" else repos)(a.update) else 0)


if __name__ == "__main__":
    main()
