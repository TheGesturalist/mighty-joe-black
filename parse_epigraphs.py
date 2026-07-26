#!/usr/bin/env python3
"""
Extract the epigraph corpus from the collected-drafts PDF into structured data.

Two source formats live in the manuscript:
  A. EPIGRAPHORISM(S)(c) front matter -- AUTHOR heading, then quote, then source.
  B. "Selected Epigraphs" interstitials -- quote, then "- Author, Work, locus".

Sections are located by textual marker, not line offset, so the parser
survives re-pagination of the source PDF.

NOTE: split("\n") -- not splitlines() -- because splitlines() also breaks
on form feeds (\x0c), which pdftotext emits at every page boundary.
"""
import re, sys, json, unicodedata
from pathlib import Path

SRC = Path(sys.argv[1] if len(sys.argv) > 1 else "full.txt")
LINES = SRC.read_text(encoding="utf-8").split("\n")

OPEN, CLOSE = "\u201c", "\u201d"
ATTR = re.compile(r"^(\s*)-\s+(.*\S)\s*$")
FOOTREF = re.compile(r"\s*\[\d+\]\s*$")

def is_upper(ch):
    return unicodedata.category(ch) == "Lu"

def unsmallcap(s):
    """pdftotext renders small caps as 'B RIAN D ILLON'. Rejoin."""
    out, i = [], 0
    while i < len(s):
        if (is_upper(s[i]) and i + 2 < len(s) and s[i+1] == " "
                and is_upper(s[i+2])
                and (i == 0 or not s[i-1].isalpha())):
            j = i + 2
            while j < len(s) and (is_upper(s[j]) or s[j] in "'’-"):
                j += 1
            if j - (i + 2) >= 2:
                out.append(s[i] + s[i+2:j]); i = j; continue
        out.append(s[i]); i += 1
    return "".join(out)

def titlecase_name(s):
    out = []
    for w in s.split():
        if re.fullmatch(r"[^\W\d_]\.?", w, re.UNICODE) and len(w) <= 2:
            out.append(w)
        elif w == w.upper():
            out.append(w[0] + w[1:].lower())
        else:
            out.append(w)
    return " ".join(out)

def find(pred, start=0):
    for i in range(start, len(LINES)):
        if pred(unsmallcap(LINES[i].replace("\f", ""))):
            return i
    return -1

records = []

def flush(author, quote, source, note, section):
    if not quote or not author:
        return
    q = re.sub(r"\s+", " ", quote).strip().strip(OPEN + CLOSE).strip()
    if len(q) < 8:
        return
    src = FOOTREF.sub("", re.sub(r"\s+", " ", source or "").strip())
    src = re.sub(r"\s+,", ",", src)
    years = re.findall(r"\b(1[5-9]\d{2}|20\d{2}|19XX)\b", src)
    records.append({
        "author": author, "quote": q, "source": src,
        "year": years[-1] if years else None,
        "note": note, "section": section,
    })

def parse_a(lo, hi, section):
    author = quote = ""; source = note = None; in_q = False
    for raw in LINES[lo:hi]:
        line = unsmallcap(raw.replace("\f", "")).rstrip()
        st = line.strip()
        if not st: continue
        m = ATTR.match(line)
        if m and not in_q and quote:
            if source is not None and len(m.group(1)) > 10:
                note = m.group(2)
            else:
                source = m.group(2)
            continue
        if st.startswith(OPEN) or in_q:
            if quote and source is not None and st.startswith(OPEN) and not in_q:
                flush(author, quote, source, note, section)
                quote, source, note = "", None, None
            quote += " " + st
            in_q = not st.rstrip().endswith(CLOSE)
            continue
        if st == st.upper() and len(st) > 2 and any(c.isalpha() for c in st):
            flush(author, quote, source, note, section)
            quote, source, note = "", None, None
            author = titlecase_name(st)
    flush(author, quote, source, note, section)

def parse_b(lo, hi, section):
    quote = ""; in_q = False
    for raw in LINES[lo:hi]:
        line = unsmallcap(raw.replace("\f", "")).rstrip()
        st = line.strip()
        if not st: continue
        m = ATTR.match(line)
        if m and quote and not in_q:
            parts = [p.strip() for p in m.group(2).split(",")]
            flush(parts[0], quote, ", ".join(parts[1:]), None, section)
            quote, in_q = "", False
            continue
        if st.startswith(OPEN) or in_q:
            quote += " " + st
            in_q = not st.rstrip().endswith(CLOSE)

# --- Section A: front-matter epigraphorisms ---------------------------
a_start = find(lambda l: "EPIGRAPHORISM" in l.upper())
a_end   = find(lambda l: "Yours, Truly Yours" in l or "Preface" in l, a_start + 1)
parse_a(a_start + 1, a_end, "Epigraphorism(s)©")

# --- Section B: every "Selected Epigraphs" interstitial ---------------
i, n = 0, 0
while True:
    i = find(lambda l: "Selected Epigraphs" in l, i + 1)
    if i == -1: break
    n += 1
    parse_b(i + 1, i + 45,
            'Selected Epigraphs — "The Collected Notebooks Vols. 4–7: The Words of Others"')

seen, uniq = set(), []
for r in records:
    k = (r["author"], r["quote"][:60])
    if k not in seen:
        seen.add(k); uniq.append(r)

sys.stderr.write(f"section A at line {a_start}-{a_end}; {n} 'Selected Epigraphs' blocks\n")
print(json.dumps(uniq, ensure_ascii=False, indent=2))
