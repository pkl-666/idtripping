#!/usr/bin/env python3
"""Record and inspect manual 9-pax availability checks."""

from __future__ import annotations

import argparse
import json
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any


DATA_DIR = Path(__file__).resolve().parent / "data"
AVAILABILITY_PATH = DATA_DIR / "availability_overrides.json"
VALID_STATUSES = {"9plus", "some", "none", "unknown"}


def load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def save_json(path: Path, payload: dict[str, Any]) -> None:
    with path.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2, sort_keys=False)
        handle.write("\n")


def load_availability_file() -> dict[str, Any]:
    if AVAILABILITY_PATH.exists():
        return load_json(AVAILABILITY_PATH)
    return {
        "source": "manual 9-pax status overrides entered by user",
        "updated_at": date.today().isoformat(),
        "notes": [
            "Use status 9plus, some, none, or unknown.",
            "This file is intentionally manual-first so the prototype can stay free.",
        ],
        "checks": [],
    }


def load_eligible_codes() -> set[str]:
    data = load_json(DATA_DIR / "eligible_airlines.json")
    return {item["code"].upper() for item in data["airlines"]}


def normalize_airport(value: str) -> str:
    value = value.strip().upper()
    if len(value) != 3:
        raise SystemExit(f"Airport code must be 3 letters: {value}")
    return value


def normalize_airline(value: str) -> str:
    value = value.strip().upper()
    if len(value) < 2:
        raise SystemExit(f"Airline code looks too short: {value}")
    return value


def add_check(args: argparse.Namespace) -> int:
    status = args.status.lower()
    if status not in VALID_STATUSES:
        raise SystemExit(f"--status must be one of: {', '.join(sorted(VALID_STATUSES))}")

    check_date = date.fromisoformat(args.date).isoformat()
    origin = normalize_airport(args.origin)
    destination = normalize_airport(args.destination)
    airline = normalize_airline(args.airline)

    eligible_codes = load_eligible_codes()
    if airline not in eligible_codes:
        print(f"Warning: {airline} is not in data/eligible_airlines.json")

    payload = load_availability_file()
    checks = payload.setdefault("checks", [])
    entry = {
        "origin": origin,
        "destination": destination,
        "airline": airline,
        "flight_number": args.flight_number.strip() if args.flight_number else None,
        "date": check_date,
        "status": status,
        "source": args.source,
        "confidence": args.confidence,
        "checked_at": datetime.now(timezone.utc).isoformat(),
        "notes": args.notes,
    }
    entry = {key: value for key, value in entry.items() if value not in (None, "")}

    replacement_index = None
    for index, existing in enumerate(checks):
        same_key = (
            existing.get("origin", "").upper() == origin
            and existing.get("destination", "").upper() == destination
            and existing.get("airline", "").upper() == airline
            and existing.get("date") == check_date
            and str(existing.get("flight_number", "")) == str(entry.get("flight_number", ""))
        )
        if same_key:
            replacement_index = index
            break

    if replacement_index is None:
        checks.append(entry)
        action = "Added"
    else:
        checks[replacement_index] = entry
        action = "Updated"

    checks.sort(
        key=lambda item: (
            item.get("date", ""),
            item.get("origin", ""),
            item.get("destination", ""),
            item.get("airline", ""),
            str(item.get("flight_number", "")),
        )
    )
    payload["updated_at"] = date.today().isoformat()
    save_json(AVAILABILITY_PATH, payload)

    print(f"{action} manual check: {check_date} {airline}{entry.get('flight_number', '')} {origin}-{destination} = {status}")
    return 0


def list_checks(args: argparse.Namespace) -> int:
    payload = load_availability_file()
    checks = payload.get("checks", [])
    if args.origin:
        origin = normalize_airport(args.origin)
        checks = [item for item in checks if item.get("origin", "").upper() == origin]
    if args.destination:
        destination = normalize_airport(args.destination)
        checks = [item for item in checks if item.get("destination", "").upper() == destination]
    if args.airline:
        airline = normalize_airline(args.airline)
        checks = [item for item in checks if item.get("airline", "").upper() == airline]

    if not checks:
        print("No manual checks found.")
        return 0

    for item in checks:
        flight = item.get("flight_number", "")
        flight_label = f"{item.get('airline', '')}{flight}" if flight else item.get("airline", "")
        print(
            f"{item.get('date', '')} | {flight_label:<8} | "
            f"{item.get('origin', '')}-{item.get('destination', '')} | "
            f"{item.get('status', 'unknown'):<7} | "
            f"{item.get('source', '')}"
        )
        if item.get("notes"):
            print(f"  notes: {item['notes']}")
    return 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Record manual 9-pax checks for ID travel tips")
    subparsers = parser.add_subparsers(dest="command", required=True)

    add = subparsers.add_parser("add", help="Add or update a manual availability check")
    add.add_argument("--date", required=True, help="Flight date, YYYY-MM-DD")
    add.add_argument("--origin", required=True, help="Origin airport, e.g. OSL")
    add.add_argument("--destination", required=True, help="Destination airport, e.g. AGP")
    add.add_argument("--airline", required=True, help="Airline code, e.g. DY")
    add.add_argument("--flight-number", help="Optional flight number, e.g. 5021")
    add.add_argument("--status", required=True, help="9plus, some, none, or unknown")
    add.add_argument("--source", default="manual 9-pax airline website check")
    add.add_argument("--confidence", default="manual")
    add.add_argument("--notes", default="")
    add.set_defaults(func=add_check)

    list_parser = subparsers.add_parser("list", help="List recorded checks")
    list_parser.add_argument("--origin")
    list_parser.add_argument("--destination")
    list_parser.add_argument("--airline")
    list_parser.set_defaults(func=list_checks)

    return parser.parse_args()


def main() -> int:
    args = parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
