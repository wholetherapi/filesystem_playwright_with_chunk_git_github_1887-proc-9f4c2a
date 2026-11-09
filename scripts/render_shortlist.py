#!/usr/bin/env python3
"""Regenerate the Seasonal shortlist section of README.md from picks.json.

Usage:
    python scripts/render_shortlist.py picks.json README.md
"""

import json
import sys
from pathlib import Path

SECTION = "## Seasonal shortlist"


def render(picks_path: str = "picks.json", readme_path: str = "README.md") -> None:
    picks = json.loads(Path(picks_path).read_text(encoding="utf-8"))
    lines = Path(readme_path).read_text(encoding="utf-8").splitlines()

    start = None
    for i, line in enumerate(lines):
        if line.strip() == SECTION:
            start = i
            break
    if start is None:
        raise SystemExit("Seasonal shortlist section not found")

    # Find the last line of the shortlist block: stop before the next heading.
    end = None
    j = start + 1
    while j < len(lines):
        if lines[j].startswith("## ") and lines[j].strip() != SECTION:
            end = j - 1
            break
        j += 1
    if end is None:
        raise SystemExit("Could not find the end of the Seasonal shortlist section")

    block = [SECTION]
    for pick in picks:
        block.append(
            "- [{title}]({url}) | AUD {price:.2f} | {seller}".format(
                title=pick["title"],
                url=pick["url"],
                price=float(pick["price"]),
                seller=pick["seller"],
            )
        )

    new_lines = lines[:start] + block + [""] + lines[end + 2 :]
    Path(readme_path).write_text("\n".join(new_lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    picks = sys.argv[1] if len(sys.argv) > 1 else "picks.json"
    readme = sys.argv[2] if len(sys.argv) > 2 else "README.md"
    render(picks, readme)
