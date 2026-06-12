#!/usr/bin/env python3
"""Read month values from publications.yaml and write them into the matching
content/publications/*.md frontmatter fields."""

from __future__ import annotations

import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
MANIFEST = ROOT / "publications.yaml"
PUB_DIR = ROOT / "src" / "content" / "publications"

_MONTH_NAMES = {
    "january": 1, "february": 2, "march": 3, "april": 4,
    "may": 5, "june": 6, "july": 7, "august": 8,
    "september": 9, "october": 10, "november": 11, "december": 12,
}


def parse_month(value) -> int | None:
    if value is None:
        return None
    if isinstance(value, int):
        return value if 1 <= value <= 12 else None
    normalized = str(value).strip().lower()
    if normalized.isdigit():
        m = int(normalized)
        return m if 1 <= m <= 12 else None
    return _MONTH_NAMES.get(normalized)


def load_month_map() -> dict[str, int]:
    with open(MANIFEST) as f:
        entries = yaml.safe_load(f)
    result: dict[str, int] = {}
    for entry in entries:
        key = entry.get("key")
        month = parse_month(entry.get("month"))
        if key and month is not None:
            result[key] = month
    return result


def set_month_in_file(path: Path, month: int) -> bool:
    text = path.read_text()
    # Extract frontmatter block between the first pair of ---
    fm_match = re.match(r"^---\n(.*?\n)---\n", text, re.DOTALL)
    if not fm_match:
        return False
    fm_text = fm_match.group(1)
    # If month already correct, skip
    existing = re.search(r"^month:\s*(\d+)\s*$", fm_text, re.MULTILINE)
    if existing and int(existing.group(1)) == month:
        return False
    if existing:
        new_fm = re.sub(r"^month:\s*\d+\s*$", f"month: {month}", fm_text, flags=re.MULTILINE)
    else:
        # Insert after year: line
        new_fm = re.sub(
            r"^(year:\s*\d+\s*\n)",
            rf"\1month: {month}\n",
            fm_text,
            count=1,
            flags=re.MULTILINE,
        )
    new_text = f"---\n{new_fm}---\n" + text[fm_match.end():]
    path.write_text(new_text)
    return True


def main() -> None:
    month_map = load_month_map()
    updated = 0
    for md_file in sorted(PUB_DIR.glob("*.md")):
        key = md_file.stem
        if key in month_map:
            if set_month_in_file(md_file, month_map[key]):
                print(f"  updated month={month_map[key]} in {md_file.name}")
                updated += 1
    print(f"enrich-months: updated {updated} file(s)")


if __name__ == "__main__":
    main()
