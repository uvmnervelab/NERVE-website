"""
One-time script: build publications.yaml for the nerve-website from the
Jekyll _data/papers.yml source.

Usage (from nerve-website root):
    python scripts/build_manifest.py

Writes publications.yaml in the project root, then you can run:
    pubman --regenerate
to (re)generate src/content/publications/*.md from the manifest.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

import yaml

JEKYLL_PAPERS = Path(__file__).parents[2] / "phd/lab_website/NERVE-website/_data/papers.yml"
OUT_MANIFEST = Path(__file__).parent.parent / "publications.yaml"


# ---------------------------------------------------------------------------
# Author name parsing
# ---------------------------------------------------------------------------

def _parse_author(raw: str) -> dict:
    """Convert a Jekyll author string to a {first, last} dict."""
    raw = raw.strip()
    if not raw:
        return {"first": "", "last": ""}
    if "," in raw:
        last, first = raw.split(",", 1)
        return {"first": first.strip(), "last": last.strip()}
    # "First Last" — last word is the last name
    parts = raw.rsplit(None, 1)
    if len(parts) == 1:
        return {"first": "", "last": parts[0]}
    return {"first": parts[0], "last": parts[1]}


# ---------------------------------------------------------------------------
# DOI extraction
# ---------------------------------------------------------------------------

_DOI_RE = re.compile(
    r"(?:https?://(?:dx\.)?doi\.org/|doi:\s*)(10\.\S+)",
    re.IGNORECASE,
)


def _extract_doi(url: str) -> str | None:
    if not url:
        return None
    m = _DOI_RE.search(url)
    if m:
        return m.group(1).rstrip("/")
    return None


# ---------------------------------------------------------------------------
# Key generation (mirrors pubman.manifest.generate_key logic)
# ---------------------------------------------------------------------------

def _generate_key(authors: list[dict], year: int, existing_keys: set) -> str:
    year_str = str(year)[-2:]
    lasts = [a["last"] for a in authors if a.get("last")]
    base = (lasts[0][:2] + lasts[1][:2] if len(lasts) >= 2 else lasts[0][:4]) + year_str
    if base not in existing_keys:
        return base
    for suffix in "abcdefghijklmnopqrstuvwxyz":
        candidate = base + suffix
        if candidate not in existing_keys:
            return candidate
    raise RuntimeError(f"Cannot generate unique key from base '{base}'")


# ---------------------------------------------------------------------------
# Main conversion
# ---------------------------------------------------------------------------

def convert() -> list:
    if not JEKYLL_PAPERS.exists():
        sys.exit(f"Jekyll papers.yml not found: {JEKYLL_PAPERS}")

    with open(JEKYLL_PAPERS) as f:
        data = yaml.safe_load(f)

    all_pubs: list = []
    for section in data.get("categories", []):
        all_pubs.extend(section.get("pubs", []))

    existing_keys: set = set()
    entries = []

    for pub in all_pubs:
        raw_authors = pub.get("author", [])
        authors = [_parse_author(str(a)) for a in raw_authors]
        if not authors:
            print(f"  Warning: no authors for '{pub.get('title', '')[:60]}'")
            continue

        year = int(pub["year"])
        key = _generate_key(authors, year, existing_keys)
        existing_keys.add(key)

        url = pub.get("url") or ""
        doi = _extract_doi(url)

        entry: dict = {
            "key": key,
            "type": "article",
            "category": "peer-reviewed",
            "title": pub["title"].replace("\n", " ").strip(),
            "authors": authors,
            "year": year,
            "featured": False,
            "image": pub.get("image_path") or None,
        }
        if pub.get("month"):
            entry["month"] = pub["month"]
        if pub.get("journal"):
            entry["journal"] = pub["journal"]
        if pub.get("volume"):
            entry["volume"] = pub["volume"]
        if pub.get("number"):
            entry["number"] = pub["number"]
        if doi:
            entry["doi"] = doi

        entries.append(entry)

    return entries


def main() -> None:
    entries = convert()
    with open(OUT_MANIFEST, "w") as f:
        yaml.dump(entries, f, allow_unicode=True, sort_keys=False,
                  default_flow_style=False, width=120)
    print(f"Wrote {len(entries)} entries → {OUT_MANIFEST}")
    print("Run `pubman --regenerate` to sync src/content/publications/")


if __name__ == "__main__":
    main()
