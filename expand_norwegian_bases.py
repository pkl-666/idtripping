#!/usr/bin/env python3
"""Add starter route data for Norwegian bases that are useful origins."""

from __future__ import annotations

import json
from datetime import date
from pathlib import Path
from typing import Any


ROUTES_PATH = Path("data/routes_sample.json")
APP_ROUTES_PATH = Path("outputs/id-travel-app/data/routes_sample.json")
DESTINATIONS_PATH = Path("data/destinations.json")
APP_DESTINATIONS_PATH = Path("outputs/id-travel-app/data/destinations.json")

TODAY = date.today().isoformat()

DESTINATIONS = [
    ("RIX", "Riga", "Latvia", ["europe", "city"]),
    ("TIV", "Tivat", "Montenegro", ["europe", "warm_europe", "beach"]),
]

ROUTES = [
    {
        "origin": "RIX",
        "destination": "OSL",
        "airline": "D8",
        "duration_min": 105,
        "source": "official Norwegian Riga destinations page",
        "source_url": "https://www.norwegian.com/en/destinations/Riga-Alldestinations",
        "source_tier": "A",
    },
    {
        "origin": "RIX",
        "destination": "ARN",
        "airline": "D8",
        "duration_min": 75,
        "source": "Riga Airport Norwegian route launch note",
        "source_url": "https://www.riga-airport.com/en/news/norwegian-launches-new-route-riga-alicante",
        "source_tier": "A",
    },
    {
        "origin": "RIX",
        "destination": "CPH",
        "airline": "D8",
        "duration_min": 85,
        "source": "Riga Airport Norwegian route launch note",
        "source_url": "https://www.riga-airport.com/en/news/norwegian-launches-new-route-riga-alicante",
        "source_tier": "A",
    },
    {
        "origin": "RIX",
        "destination": "ALC",
        "airline": "D8",
        "duration_min": 250,
        "source": "official Norwegian Riga-Alicante low fare calendar",
        "source_url": "https://www.norwegian.com/uk/low-fare-calendar/Riga-Alicante",
        "source_tier": "A",
    },
    {
        "origin": "RIX",
        "destination": "CFU",
        "airline": "D8",
        "duration_min": 185,
        "source": "Riga Airport Norwegian route launch note",
        "source_url": "https://www.riga-airport.com/en/news/norwegian-launches-new-route-riga-alicante",
        "source_tier": "A",
    },
    {
        "origin": "RIX",
        "destination": "TIV",
        "airline": "D8",
        "duration_min": 165,
        "source": "Riga Airport Norwegian route launch note",
        "source_url": "https://www.riga-airport.com/en/news/norwegian-launches-new-route-riga-alicante",
        "source_tier": "A",
    },
    {
        "origin": "BGO",
        "destination": "RIX",
        "airline": "D8",
        "duration_min": 115,
        "source": "Bergen-Riga schedule reference",
        "source_url": "https://www.flightsfrom.com/BGO-RIX",
        "source_tier": "B",
    },
]


def load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def save_json(path: Path, payload: dict[str, Any]) -> None:
    with path.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2, ensure_ascii=False)
        handle.write("\n")


def add_destinations() -> int:
    payload = load_json(DESTINATIONS_PATH)
    existing = {item["iata"] for item in payload["destinations"]}
    added = 0
    for iata, city, country, regions in DESTINATIONS:
        if iata in existing:
            continue
        payload["destinations"].append({"iata": iata, "city": city, "country": country, "regions": regions})
        existing.add(iata)
        added += 1
    payload["updated_at"] = TODAY
    save_json(DESTINATIONS_PATH, payload)
    save_json(APP_DESTINATIONS_PATH, payload)
    return added


def add_routes() -> int:
    payload = load_json(ROUTES_PATH)
    existing = {(item["origin"], item["destination"], item["airline"]) for item in payload["legs"]}
    added = 0
    for route in ROUTES:
        key = (route["origin"], route["destination"], route["airline"])
        if key in existing:
            continue
        payload["legs"].append({
            **route,
            "confidence": "official_source_candidate",
            "verified_at": "",
            "route_confidence": "medium",
        })
        existing.add(key)
        added += 1
    payload["updated_at"] = TODAY
    save_json(ROUTES_PATH, payload)
    save_json(APP_ROUTES_PATH, payload)
    return added


def main() -> int:
    print(f"Added {add_destinations()} destination(s).")
    print(f"Added {add_routes()} route leg(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
