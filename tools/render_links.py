#!/usr/bin/env python3
"""
Render data/links.csv into docs/apparatus/toolshed.md.

Source today is a Google Sheet export. When the corpus moves to Grist,
replace read_source() with a Grist API pull -- everything downstream
is unchanged.

Grist:  GET {GRIST_URL}/api/docs/{DOC_ID}/tables/{TABLE}/records
        header: Authorization: Bearer {GRIST_API_KEY}
"""
import re, csv, sys
from pathlib import Path
from collections import defaultdict
from urllib.parse import urlparse

SRC = Path("data/links.csv")
OUT = Path("docs/apparatus/toolshed.md")

SECTIONS = {
    "mkdocs/catalog":            ("MkDocs Plugins & Projects", "Machinery for this site itself."),
    "best-of-digital-gardens":   ("Digital Gardens",           "Other people's public notebooks. Read these for form, not content."),
    "AwesomeCSV":                ("CSV & Tabular Tooling",     "For getting data out of spreadsheets and into pages."),
}

def section_for(source_title):
    for key, val in SECTIONS.items():
        if key.lower() in str(source_title).lower():
            return val
    return ("Unsorted", "Not yet filed.")

def is_cruft(title, url, source_url):
    t = str(title).strip()
    if not t or t.lower() == "nan":                 return True
    if re.fullmatch(r"[`~\-_.\s]+", t):             return True   # backtick fences
    if re.match(r"^(MIT|Apache|BSD|GPL|LGPL|MPL|ISC|Unlicense|CC0|Public Domain)\b", t, re.I): return True
    if "bit.ly" in str(url) or "pypi.org" in str(url): return True
    if len(t) < 2:                                  return True
    base = lambda u: str(u).split("#")[0].rstrip("/")
    if "#" in str(url) and base(url) == base(source_url):  return True  # anchor into own TOC
    if "raw.githubusercontent.com" in str(url):     return True
    return False

rows = list(csv.DictReader(SRC.open(encoding="utf-8")))
buckets, seen, dropped = defaultdict(list), set(), 0

for r in rows:
    title, url = r.get("Title"), r.get("Url", "")
    if is_cruft(title, url, r.get("Source.Url", "")):
        dropped += 1; continue
    if url in seen:
        dropped += 1; continue
    seen.add(url)
    name, blurb = section_for(r.get("Source.Title"))
    buckets[(name, blurb)].append((str(title).strip(), url, urlparse(url).netloc))

total = sum(len(v) for v in buckets.values())

L = ["---", "title: Toolshed", "relational_density: 0.4",
     "tags:", "  - apparatus", "  - tooling", "---", "",
     "# Toolshed", "",
     "!!! warning \"This is a tooling index, not a humanities bibliography\"",
     "    Harvested from three curated lists. It is machinery — what the site is",
     "    built out of, not what it is about. Scholarly sources live in the",
     "    [Encyclopedia](../encyclopedia/index.md).", "",
     f"**{total} entries**, generated from `data/links.csv`. "
     f"{dropped} rows dropped as navigational cruft, duplicates, or untitled. "
     "Do not edit this page by hand — edit the source table and rebuild.", ""]

for (name, blurb) in sorted(buckets, key=lambda k: -len(buckets[k])):
    items = sorted(buckets[(name, blurb)], key=lambda x: x[0].lower())
    L += [f"## {name}", "", f"*{blurb}* — {len(items)} entries", "",
          "| Tool | Host |", "|---|---|"]
    for title, url, host in items:
        safe = title.replace("|", "\\|")
        L.append(f"| [{safe}]({url}) | `{host}` |")
    L.append("")

L += ["*[Note: No visual elements or graphics are currently present on this page]*", ""]
OUT.write_text("\n".join(L), encoding="utf-8")
print(f"wrote {OUT} — {total} kept, {dropped} dropped, {len(buckets)} sections")
