#!/usr/bin/env python3
"""Detect upstream drift so the skill can evolve (stdlib + curl + git).

  refresh.py docs            re-fetch analogue.co developer docs, report changed / new / vanished pages
  refresh.py docs --update   ...and overwrite references/docs-snapshot with the fresh text
  refresh.py repos           compare watched GitHub repos' HEAD against sources.json, report new commits
  refresh.py repos --update  record the new HEADs
  refresh.py toolchain       re-read the Quartus edition/device support chart (Macnica mirror of Altera's table) and compare with
                             references/knowledge-base/toolchain-baseline.json (Cyclone V in Lite/Standard/Pro, new versions)
  refresh.py edition FILE    read a Quartus report (ap_core.fit.rpt or .map.rpt): edition, version, whether physical-synthesis
                             options (retiming, duplication) were ON and actually applied. Use it to test edition claims on YOUR build.
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


BASELINE = os.path.join(ROOT, "references", "knowledge-base", "toolchain-baseline.json")


def _table_rows(tb):
    return [[html.unescape(re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", c))).replace("\u200b", "").strip()
             for c in re.findall(r"<t[hd].*?</t[hd]>", tr, flags=re.S)] for tr in re.findall(r"<tr.*?</tr>", tb, flags=re.S)]


def read_chart(url):
    code, raw = fetch(url)
    if code != "200":
        sys.exit(f"chart fetch failed: HTTP {code} {url}")
    tabs = re.findall(r"<table.*?</table>", raw, flags=re.S)
    if len(tabs) < 2:
        sys.exit("chart layout changed (expected 2 tables): update read_chart()")
    pro, sl = _table_rows(tabs[0]), _table_rows(tabs[1])
    ok = ("\u25cf", "\u2605")  # filled circle, star = supported
    pro_fam = [r[0] for r in pro[1:]]
    cv = [r for r in sl[2:] if re.search(r"Cyclone\W*V", r[0]) and "10" not in r[0] and "IV" not in r[0]]
    std = cv[0][1::2] if cv else []
    lite = cv[0][2::2] if cv else []
    return {
        "pro_families": [re.sub(r"\s+", " ", f) for f in pro_fam],
        "pro_latest_version": pro[0][2] if len(pro[0]) > 2 else "?",
        "std_lite_latest_version": sl[0][2] if len(sl[0]) > 2 else "?",
        "cyclone_v_in_pro": any(re.search(r"Cyclone\W*V", f) and "10" not in f for f in pro_fam),
        "cyclone_v_standard_all_versions": bool(std) and all(c in ok for c in std),
        "cyclone_v_lite_all_versions": bool(lite) and all(c in ok for c in lite),
        "lite_supported_families": [re.sub(r"\s+", " ", r[0]) for r in sl[2:] if any(c in ok for c in r[2::2])],
        "standard_only_families": [re.sub(r"\s+", " ", r[0]) for r in sl[2:] if any(c in ok for c in r[1::2]) and not any(c in ok for c in r[2::2])],
    }


def toolchain(update):
    src = json.load(open(SRC))
    cur = read_chart(src["toolchain"]["chart"])
    base = json.load(open(BASELINE)) if os.path.exists(BASELINE) else None
    print("Cyclone V: Pro=%s Standard=%s Lite=%s (Lite families: %s)" % (
        cur["cyclone_v_in_pro"], cur["cyclone_v_standard_all_versions"], cur["cyclone_v_lite_all_versions"], ", ".join(cur["lite_supported_families"])))
    changed = base is not None and base != cur
    if base is None:
        print("no baseline yet")
    elif changed:
        for k in cur:
            if base.get(k) != cur[k]:
                print(f"CHANGED {k}: {base.get(k)} -> {cur[k]}")
    else:
        print("toolchain support chart: no change")
    if update or base is None:
        json.dump(cur, open(BASELINE, "w"), indent=2); print("baseline written")
    return changed


def edition(path):
    txt = open(path, encoding="utf-8", errors="ignore").read()
    ver = re.search(r"Quartus Prime Version\s*;?\s*([^;\n]+)", txt)
    print("version:", ver.group(1).strip() if ver else "not found")
    print("edition:", "Lite" if "Lite Edition" in txt else "Standard/Pro? (no 'Lite Edition' string)")
    for k in ("Perform Register Retiming for Performance", "Perform Register Duplication for Performance",
              "Perform Physical Synthesis for Combinational Logic for Performance", "Physical Synthesis Effort Level", "Fitter Effort"):
        m = re.search(re.escape(k) + r"\s*;\s*([^;]+);", txt)
        print(f"{k}: {m.group(1).strip() if m else 'not in this report'}")
    print("registers retimed by the fitter:", len(re.findall(r"Retimed Register", txt)), "(0 with the option ON would mean it was not applied)")
    return False


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("what", choices=["docs", "repos", "toolchain", "edition"]); ap.add_argument("file", nargs="?"); ap.add_argument("--update", action="store_true")
    a = ap.parse_args()
    if a.what == "edition":
        if not a.file:
            sys.exit("usage: refresh.py edition path/to/ap_core.fit.rpt")
        sys.exit(2 if edition(a.file) else 0)
    sys.exit(2 if {"docs": docs, "repos": repos, "toolchain": toolchain}[a.what](a.update) else 0)


if __name__ == "__main__":
    main()
