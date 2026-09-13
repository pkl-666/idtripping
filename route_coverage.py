#!/usr/bin/env python3
"""Report which eligible airlines are represented in the route graph."""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path


DATA_DIR = Path("data")


def load_json(path: Path) -> dict:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def main() -> int:
    eligible = load_json(DATA_DIR / "eligible_airlines.json")["airlines"]
    routes = load_json(DATA_DIR / "routes_sample.json")["legs"]
    counts = Counter(route["airline"] for route in routes)

    covered = [(item["code"], item["name"], counts[item["code"]]) for item in eligible if counts[item["code"]]]
    missing = [(item["code"], item["name"]) for item in eligible if not counts[item["code"]]]

    print(f"Eligible airlines: {len(eligible)}")
    print(f"Covered airlines: {len(covered)}")
    print(f"Missing airlines: {len(missing)}")
    print()
    print("Covered:")
    for code, name, count in sorted(covered, key=lambda row: (-row[2], row[0])):
        print(f"  {code:>3} {name} ({count})")
    print()
    print("Missing:")
    for code, name in missing:
        print(f"  {code:>3} {name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
