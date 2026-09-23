#!/usr/bin/env python3
"""One-command release for this skill: validate, review, commit, push, rebuild the .skill file.

  release.py                 interactive: shows what changed, asks before commit and before push
  release.py --dry-run       validate + show what would happen; changes nothing
  release.py --yes -m "msg"  non-interactive (commit + push without prompting)
  release.py --no-push       commit only            release.py --no-package   skip the .skill build
  release.py --out DIR       where to write analogue-pocket-dev.skill (default ~/Downloads)

Only committed content goes into the .skill (built from `git archive HEAD`), so git-ignored local
files (private entries, downloaded Analogue docs) can never be packaged. After a release, re-upload
the .skill in Claude.ai (Settings > Skills): that copy never updates itself.
"""
import argparse, glob, os, subprocess, sys, tempfile, zipfile

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
NAME = "analogue-pocket-dev"


def run(*cmd, check=True, cwd=ROOT):
    r = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    if check and r.returncode:
        sys.exit(f"FAILED: {' '.join(cmd)}\n{r.stdout}{r.stderr}")
    return r


def ask(q, yes):
    if yes:
        return True
    if not sys.stdin.isatty():
        print(f"{q} -> not interactive; pass --yes to proceed. Stopping here.")
        return False
    return input(f"{q} [y/N] ").strip().lower() in ("y", "yes")


def package(out):
    with tempfile.TemporaryDirectory() as tmp:
        tar = os.path.join(tmp, "src.tar")
        run("git", "archive", "--format=tar", f"--prefix={NAME}/", "-o", tar, "HEAD")
        run("tar", "-xf", tar, "-C", tmp)
        skill_dir = os.path.join(tmp, NAME)
        os.makedirs(out, exist_ok=True)
        dst = os.path.join(out, f"{NAME}.skill")
        if os.path.exists(dst):
            os.remove(dst)
        pk = glob.glob(os.path.expanduser("~/Library/Application Support/Claude/**/skill-creator/scripts/package_skill.py"), recursive=True)
        if pk:  # official packager (validates frontmatter); needs pyyaml
            r = run(sys.executable, "-m", "scripts.package_skill", skill_dir, out, check=False, cwd=os.path.dirname(os.path.dirname(pk[0])))
            if r.returncode == 0 and os.path.exists(dst):
                return dst
            out_ = (r.stdout or "") + (r.stderr or "")
            if "Validation failed" in out_:  # do not ship something Claude.ai's validator would reject
                sys.exit("packaging refused: " + [l for l in out_.splitlines() if "Validation failed" in l][0].strip())
            print("official packager unavailable, using built-in zip:", out_.strip().splitlines()[-1:])
        with zipfile.ZipFile(dst, "w", zipfile.ZIP_DEFLATED) as z:
            for base, _, files in os.walk(skill_dir):
                for f in files:
                    p = os.path.join(base, f)
                    z.write(p, os.path.relpath(p, tmp))
        return dst


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--dry-run", action="store_true"); ap.add_argument("--yes", action="store_true")
    ap.add_argument("-m", "--message"); ap.add_argument("--no-push", action="store_true")
    ap.add_argument("--no-package", action="store_true"); ap.add_argument("--out", default=os.path.expanduser("~/Downloads"))
    a = ap.parse_args()

    if run("git", "rev-parse", "--is-inside-work-tree", check=False).returncode:
        sys.exit("not a git checkout")
    branch = run("git", "rev-parse", "--abbrev-ref", "HEAD").stdout.strip()
    print(f"== 1/5 validate ({branch})")
    v = run(sys.executable, "scripts/kb.py", "validate", check=False)
    print(v.stdout.strip())
    if v.returncode:
        sys.exit("validate failed: fix the errors above (guards protect claims and keep private text out); nothing was changed")
    run(sys.executable, "scripts/kb.py", "index")
    import re as _re
    _fm = _re.match(r"---\n.*?description: \"(.*?)\"\n---", open(os.path.join(ROOT, "SKILL.md"), encoding="utf-8").read(), _re.S)
    if _fm and (len(_fm.group(1)) > 1024 or "<" in _fm.group(1) or ">" in _fm.group(1)):
        sys.exit(f"SKILL.md description is {len(_fm.group(1))} chars (limit 1024, no angle brackets): shorten it")

    print("== 2/5 changes")
    st = run("git", "status", "--short").stdout
    print(st.strip() or "(working tree clean)")
    if st.strip():
        print(run("git", "diff", "--stat", "HEAD").stdout.strip())
    has_remote = run("git", "remote", check=False).stdout.strip() != ""
    behind = 0
    if has_remote:
        run("git", "fetch", "-q", check=False)
        behind = int(run("git", "rev-list", "--count", f"HEAD..origin/{branch}", check=False).stdout.strip() or 0)
        if behind:
            sys.exit(f"remote has {behind} commit(s) you do not have: run `git pull --rebase` first, then release again")
    if a.dry_run:
        print("\n--dry-run: would commit" + ("" if a.no_push else " + push") + ("" if a.no_package else " + build .skill") + ". Nothing changed.")
        return

    committed = False
    if st.strip():
        print("== 3/5 commit")
        if ask("Commit these changes?", a.yes):
            msg = a.message or (input("Commit message: ").strip() if sys.stdin.isatty() and not a.yes else "Update knowledge base")
            msg += "\n\nCo-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>"
            run("git", "add", "-A")
            r = run("git", "commit", "-q", "-m", msg, check=False)
            if r.returncode:
                sys.exit("commit refused (pre-commit guard?):\n" + r.stdout + r.stderr)
            committed = True
            print(run("git", "log", "--oneline", "-1").stdout.strip())
        else:
            sys.exit("stopped before commit; nothing pushed or packaged")
    else:
        print("== 3/5 commit: nothing to commit")

    ahead = int(run("git", "rev-list", "--count", f"origin/{branch}..HEAD", check=False).stdout.strip() or 0) if has_remote else 0
    if a.no_push or not has_remote:
        print("== 4/5 push: skipped")
    elif ahead == 0:
        print("== 4/5 push: nothing to push")
    else:
        print(f"== 4/5 push ({ahead} commit(s) to public remote)")
        print(run("git", "log", "--oneline", f"origin/{branch}..HEAD").stdout.strip())
        if ask("Push to the remote (this is publicly visible if the repo is public)?", a.yes):
            r = run("git", "push", check=False)
            print((r.stdout + r.stderr).strip().splitlines()[-1] if (r.stdout + r.stderr).strip() else "pushed")
            if r.returncode:
                sys.exit("push failed")
        else:
            print("not pushed")

    if a.no_package:
        print("== 5/5 package: skipped")
    else:
        print("== 5/5 package (committed content only)")
        print("wrote", package(a.out))
        print("Re-upload this file in Claude.ai (Settings > Skills) if you use the skill there; that copy does not auto-update.")


if __name__ == "__main__":
    main()
