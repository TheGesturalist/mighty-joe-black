#!/usr/bin/env python3
"""Render data/epigraphs.json into docs/apparatus/epigraphs.md."""
import json, re, unicodedata
from pathlib import Path
from collections import defaultdict

DATA = json.loads(Path("data/epigraphs.json").read_text(encoding="utf-8"))
OUT = Path("docs/apparatus/epigraphs.md")

def slug(s):
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")

by_author = defaultdict(list)
for r in DATA:
    by_author[r["author"]].append(r)

L = []
L.append("---")
L.append("title: Epigraph Concordance")
L.append("relational_density: 0.9")
L.append("tags:")
L.append("  - apparatus")
L.append("  - concordance")
L.append("---")
L.append("")
L.append("# Epigraph Concordance")
L.append("")
L.append("!!! quote \"On the form\"")
L.append("    The epigraphs here are categorised by writer rather than by quotation,")
L.append("    because there are many, and one writer may hold more than one")
L.append("    *epigraphorism©*. See [Epigraphorism©](lexicon.md#epigraphorism) in the")
L.append("    Lexicon. — *J. L. Roapes*")
L.append("")
L.append(f"**{len(DATA)} epigraphs · {len(by_author)} writers.** "
         "Generated from the collected drafts — do not edit by hand; "
         "edit the source and rebuild. Every entry has a permanent anchor, so any "
         "line here can be linked from anywhere else on the site.")
L.append("")
L.append("---")
L.append("")

for author in sorted(by_author, key=lambda a: a.split()[-1]):
    entries = by_author[author]
    L.append(f"## {author} {{ #{slug(author)} }}")
    L.append("")
    for e in entries:
        anchor = slug(author + "-" + e["quote"][:32])
        L.append(f'> "{e["quote"]}"')
        L.append("")
        cite = e["source"] or "—"
        L.append(f'<cite id="{anchor}">{cite}</cite>')
        if e.get("note"):
            L.append(f"<br><small>— {e['note']}</small>")
        L.append("")
        L.append(f"[:material-link: permalink](#{anchor}){{ .md-button .md-button--sm }}"
                 if False else "")
    L.append("")

L.append("---")
L.append("")
L.append("## Index by year")
L.append("")
L.append("| Year | Writer | Source |")
L.append("|---:|---|---|")
for e in sorted(DATA, key=lambda r: (r["year"] or "9999")):
    L.append(f'| {e["year"] or "—"} | [{e["author"]}](#{slug(e["author"])}) | {e["source"] or "—"} |')
L.append("")
L.append("## Sources of these sources")
L.append("")
secs = sorted({e["section"] for e in DATA})
for s in secs:
    n = sum(1 for e in DATA if e["section"] == s)
    L.append(f"- **{s}** — {n} entries")
L.append("")
L.append("*[Note: No visual elements or graphics are currently present on this page]*")
L.append("")

OUT.write_text("\n".join(l for l in L if l is not None), encoding="utf-8")
print(f"wrote {OUT} — {len(DATA)} epigraphs, {len(by_author)} writers")
