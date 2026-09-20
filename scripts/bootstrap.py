#!/usr/bin/env python3
"""Fetch third-party reference material locally (not redistributed in this repo).

  bootstrap.py   download Analogue developer docs (as text) into references/docs-snapshot/
                 and selected open-fpga source files into references/repo-src/
Needs: curl, git. Safe to re-run. Content stays local and is git-ignored.
"""
import json, os, shutil, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import refresh  # noqa: E402

ROOT = refresh.ROOT
man = json.load(open(os.path.join(ROOT, "references", "docs-manifest.json")))
os.makedirs(refresh.SNAP, exist_ok=True)
ok = bad = 0
for path in man["pages"]:
    code, raw = refresh.fetch(man["base"] + path)
    name = ("overview" if path.endswith("/overview") else path.replace("/developer/docs/", "").replace("/", "__")) + ".txt"
    if code != "200":
        print("FAILED", path, code); bad += 1; continue
    open(os.path.join(refresh.SNAP, name), "w", encoding="utf-8").write(refresh.extract(raw)); ok += 1
print(f"docs: {ok} fetched, {bad} failed -> references/docs-snapshot/")

dst = os.path.join(ROOT, "references", "repo-src")
os.makedirs(dst, exist_ok=True)
for item in man["repo_src"]:
    tmp = tempfile.mkdtemp()
    r = subprocess.run(["git", "clone", "-q", "--depth", "1", item["repo"], tmp], capture_output=True, text=True)
    if r.returncode:
        print("FAILED clone", item["repo"]); continue
    for src, out in item["files"].items():
        shutil.copy(os.path.join(tmp, src), os.path.join(dst, out))
    shutil.rmtree(tmp)
    print("repo-src:", item["repo"].split("/")[-1], "ok")
print("Done. Analogue's docs/APF code are subject to Analogue's own licenses; keep them local.")
