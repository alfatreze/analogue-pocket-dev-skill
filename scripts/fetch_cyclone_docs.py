#!/usr/bin/env python3
"""Fetch Cyclone V reference documentation into references/docs-snapshot/cyclone-v/ (local only, git-ignored).

The content is copyrighted by Altera/Intel and must never be committed or published; this script only
holds URLs and the fetch logic. Needs: curl; pypdf (pip install pypdf) only for the PDF text conversion.
  fetch_cyclone_docs.py            Altera docs-site books (Device Handbook Vol 1, Datasheet, Overview, GX/GT/E errata)
                                   as text, plus the two Cornell-hosted PDFs (Cyclone V handbook, DSP white paper)
Altera's docs site is a Fluid Topics app: the public /api/khub/maps/<id>/toc and .../topics/<id>/content
endpoints return the topic HTML, which is stripped to text. Map ids come from /api/khub/maps?limit=5000.
Safe to re-run (overwrites).
"""
import html, json, os, re, subprocess, sys, time
from concurrent.futures import ThreadPoolExecutor

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "references", "docs-snapshot", "cyclone-v")
SITE = "https://docs.altera.com"
BOOKS = [  # (khub map id, file name)
    ("dvxWxDO1_JfCNh~DgmxAcw", "cyclone-v-device-handbook-vol1"),
    ("ntTO5vJ6KDUXytXn~tlAoA", "cyclone-v-device-datasheet"),
    ("uAn6p8hXRtTLPEJMe3CTsw", "cyclone-v-device-overview"),
    ("SO8ju~WVb_sYzfb3~vz5xw", "cyclone-v-gx-gt-e-errata"),
]
PDFS = [
    "https://people.ece.cornell.edu/land/courses/ece5760/DE1_SOC/cyclone5_handbook.pdf",
    "https://people.ece.cornell.edu/land/courses/ece5760/DE1_SOC/DSP_wp-01159-arriav-cyclonev-dsp.pdf",
]


def curl(url, out=None):
    cmd = ["curl", "-sL", "-A", "Mozilla/5.0", "-m", "300"] + (["-o", out] if out else []) + [url]
    return subprocess.run(cmd, capture_output=True).stdout


def strip(raw):
    h = re.sub(r"(?is)<(script|style).*?</\1>", "", raw.decode("utf8", "replace"))
    h = re.sub(r"(?i)<br\s*/?>|</(p|div|tr|li|h\d|table|pre)>", "\n", h)
    h = re.sub(r"(?i)</t[dh]>", " | ", h)
    h = html.unescape(re.sub(r"<[^>]+>", "", h))
    return re.sub(r"\n\s*\n+", "\n\n", re.sub(r"[ \t]+", " ", h)).strip()


def flat(toc, depth=0, out=None):
    out = [] if out is None else out
    for e in toc:
        out.append((depth, e.get("title", ""), e.get("contentId")))
        flat(e.get("children", []), depth + 1, out)
    return out


def book(mid, name):
    items = flat(json.loads(curl(f"{SITE}/api/khub/maps/{mid}/toc")))

    def one(it):
        d, t, c = it
        if not c:
            return d, t, ""
        for _ in range(3):
            b = curl(f"{SITE}/api/khub/maps/{mid}/topics/{c}/content")
            if len(b) > 50:
                return d, t, strip(b)
        return d, t, "[FETCH FAILED]"

    with ThreadPoolExecutor(8) as ex:
        res = list(ex.map(one, items))
    with open(os.path.join(OUT, "altera", name + ".txt"), "w", encoding="utf-8") as o:
        o.write(f"# {name}\n# source: {SITE}/api/khub/maps/{mid} (fetched {time.strftime('%F')})\n"
                "# LOCAL COPY ONLY: copyrighted, never publish\n")
        for d, t, x in res:
            o.write("\n" + "#" * (d + 1) + " " + t + "\n\n" + x + "\n")
    print(name, len(res), "topics,", sum(r[2] == "[FETCH FAILED]" for r in res), "failed")


def pdf(url):
    path = os.path.join(OUT, url.rsplit("/", 1)[1])
    curl(url, path)
    try:
        import pypdf
    except ImportError:
        print("pypdf missing: kept", path, "without text (pip install pypdf)")
        return
    r = pypdf.PdfReader(path)
    with open(path[:-4] + ".txt", "w", encoding="utf-8") as o:
        o.write(f"# {os.path.basename(path)} (local copy only, copyrighted, never publish; source {url})\n")
        for i, p in enumerate(r.pages):
            try:
                t = p.extract_text() or ""
            except Exception as e:  # noqa: BLE001
                t = f"[extract failed: {e}]"
            o.write(f"\n\n=== page {i + 1}/{len(r.pages)} ===\n{t}")
    print(os.path.basename(path), len(r.pages), "pages")


if __name__ == "__main__":
    os.makedirs(os.path.join(OUT, "altera"), exist_ok=True)
    for mid, name in BOOKS:
        book(mid, name)
    for u in PDFS:
        pdf(u)
    sys.exit(0)
