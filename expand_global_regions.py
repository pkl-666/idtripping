#!/usr/bin/env python3
"""Add Oceania, Japan, Caribbean and richer Middle East hub routing."""

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

SOURCE = {
    "AA": ("official American Airlines where-we-fly page", "https://www.aa.com/en-us/where-we-fly"),
    "AC": ("official Air Canada sunny destinations page", "https://www.aircanada.com/en-us/flights-to-sun-destinations"),
    "AY": ("official Finnair Japan destinations page", "https://www.finnair.com/jp-en/destinations/asia-pacific/japan"),
    "BA": ("official British Airways Caribbean page", "https://www.britishairways.com/content/en/gb/flights/caribbean"),
    "B6": ("official JetBlue route map", "https://www.jetblue.com/route-map"),
    "EK": ("official Emirates route map", "https://routemap.emirates.com/ae/english/"),
    "EY": ("official Etihad destinations page", "https://www.etihad.com/en-us/destinations"),
    "QR": ("official Qatar Airways destinations page", "https://www.qatarairways.com/en/destinations.html"),
    "RJ": ("official Royal Jordanian destinations page", "https://www.rj.com/en/plan-and-book/destinations"),
    "SV": ("official Saudia destinations page", "https://www.saudia.com/pages/destinations"),
    "WY": ("official Oman Air destinations page", "https://services.omanair.com/om/en/oman-air-destinations"),
}

DESTINATIONS = [
    ("ADL", "Adelaide", "Australia", ["oceania", "australia", "city", "warm"]),
    ("AKL", "Auckland", "New Zealand", ["oceania", "city", "island"]),
    ("ANU", "Antigua", "Antigua and Barbuda", ["caribbean", "beach", "island", "warm"]),
    ("AUA", "Aruba", "Aruba", ["caribbean", "beach", "island", "warm"]),
    ("BGI", "Bridgetown", "Barbados", ["caribbean", "beach", "island", "warm"]),
    ("BNE", "Brisbane", "Australia", ["oceania", "australia", "city", "warm"]),
    ("CUN", "Cancun", "Mexico", ["caribbean", "beach", "warm"]),
    ("CMB", "Colombo", "Sri Lanka", ["asia", "indian_ocean", "beach", "island", "warm"]),
    ("CUR", "Curaçao", "Curaçao", ["caribbean", "beach", "island", "warm"]),
    ("HND", "Tokyo Haneda", "Japan", ["asia", "japan", "city"]),
    ("HKT", "Phuket", "Thailand", ["asia", "beach", "island", "warm"]),
    ("KIX", "Osaka Kansai", "Japan", ["asia", "japan", "city"]),
    ("KUL", "Kuala Lumpur", "Malaysia", ["asia", "city", "warm"]),
    ("MBJ", "Montego Bay", "Jamaica", ["caribbean", "beach", "island", "warm"]),
    ("MCT", "Muscat", "Oman", ["middle_east", "city", "warm"]),
    ("MEL", "Melbourne", "Australia", ["oceania", "australia", "city"]),
    ("MNL", "Manila", "Philippines", ["asia", "city", "warm", "island"]),
    ("NAN", "Nadi", "Fiji", ["oceania", "beach", "island", "warm"]),
    ("NAS", "Nassau", "Bahamas", ["caribbean", "beach", "island", "warm"]),
    ("NRT", "Tokyo Narita", "Japan", ["asia", "japan", "city"]),
    ("PER", "Perth", "Australia", ["oceania", "australia", "city", "warm"]),
    ("PUJ", "Punta Cana", "Dominican Republic", ["caribbean", "beach", "warm"]),
    ("RUH", "Riyadh", "Saudi Arabia", ["middle_east", "city", "warm"]),
    ("SEZ", "Mahé", "Seychelles", ["indian_ocean", "beach", "island", "warm"]),
    ("SIN", "Singapore", "Singapore", ["asia", "city", "warm"]),
    ("SJU", "San Juan", "Puerto Rico", ["caribbean", "beach", "island", "warm"]),
    ("SYD", "Sydney", "Australia", ["oceania", "australia", "city", "beach"]),
    ("UVF", "St Lucia Hewanorra", "Saint Lucia", ["caribbean", "beach", "island", "warm"]),
]

ROUTES = [
    # More Middle East access from existing European hubs.
    ("LHR", "MCT", "WY", 440),
    ("FRA", "MCT", "WY", 405),
    ("MUC", "MCT", "WY", 390),
    ("CDG", "MCT", "WY", 420),
    ("IST", "MCT", "WY", 300),
    ("ZRH", "MCT", "WY", 395),
    ("LHR", "RUH", "SV", 390),
    ("FRA", "RUH", "SV", 365),
    ("CDG", "RUH", "SV", 375),
    ("LHR", "AMM", "RJ", 315),
    ("CDG", "AMM", "RJ", 285),
    ("FRA", "AMM", "RJ", 260),
    # Oman Air beyond Muscat.
    ("MCT", "BKK", "WY", 370),
    ("MCT", "HKT", "WY", 390),
    ("MCT", "KUL", "WY", 405),
    ("MCT", "MNL", "WY", 535),
    ("MCT", "CMB", "WY", 240),
    ("MCT", "MLE", "WY", 220),
    ("MCT", "DEL", "WY", 190),
    ("MCT", "BOM", "WY", 160),
    # Emirates: Oceania/Japan/Indian Ocean.
    ("DXB", "ADL", "EK", 780),
    ("DXB", "AKL", "EK", 960),
    ("DXB", "BNE", "EK", 840),
    ("DXB", "CMB", "EK", 260),
    ("DXB", "HND", "EK", 585),
    ("DXB", "KIX", "EK", 560),
    ("DXB", "KUL", "EK", 430),
    ("DXB", "MEL", "EK", 815),
    ("DXB", "NRT", "EK", 585),
    ("DXB", "PER", "EK", 645),
    ("DXB", "SEZ", "EK", 275),
    ("DXB", "SIN", "EK", 455),
    ("DXB", "SYD", "EK", 840),
    # Qatar: Oceania/Japan/Asia.
    ("DOH", "ADL", "QR", 790),
    ("DOH", "AKL", "QR", 1030),
    ("DOH", "BNE", "QR", 850),
    ("DOH", "HND", "QR", 590),
    ("DOH", "KIX", "QR", 560),
    ("DOH", "KUL", "QR", 440),
    ("DOH", "MEL", "QR", 830),
    ("DOH", "NRT", "QR", 590),
    ("DOH", "PER", "QR", 650),
    ("DOH", "SEZ", "QR", 300),
    ("DOH", "SIN", "QR", 465),
    ("DOH", "SYD", "QR", 845),
    # Etihad: Oceania/Japan/Asia.
    ("AUH", "HND", "EY", 585),
    ("AUH", "KIX", "EY", 560),
    ("AUH", "KUL", "EY", 430),
    ("AUH", "MEL", "EY", 810),
    ("AUH", "NRT", "EY", 585),
    ("AUH", "SEZ", "EY", 275),
    ("AUH", "SIN", "EY", 455),
    ("AUH", "SYD", "EY", 835),
    # Finnair/Japan: useful non-Middle-East alternative from Scandinavia.
    ("HEL", "HND", "AY", 780),
    ("HEL", "KIX", "AY", 760),
    ("HEL", "NRT", "AY", 780),
    # Caribbean via London, Miami, Toronto/New York.
    ("LHR", "ANU", "BA", 510),
    ("LHR", "BGI", "BA", 530),
    ("LHR", "CUN", "BA", 510),
    ("LHR", "MBJ", "BA", 585),
    ("LHR", "NAS", "BA", 560),
    ("LHR", "PUJ", "BA", 555),
    ("LHR", "UVF", "BA", 510),
    ("MIA", "ANU", "AA", 210),
    ("MIA", "AUA", "AA", 180),
    ("MIA", "BGI", "AA", 230),
    ("MIA", "CUN", "AA", 110),
    ("MIA", "CUR", "AA", 180),
    ("MIA", "MBJ", "AA", 105),
    ("MIA", "NAS", "AA", 65),
    ("MIA", "PUJ", "AA", 140),
    ("MIA", "SJU", "AA", 150),
    ("YYZ", "ANU", "AC", 300),
    ("YYZ", "AUA", "AC", 310),
    ("YYZ", "BGI", "AC", 320),
    ("YYZ", "CUN", "AC", 250),
    ("YYZ", "CUR", "AC", 315),
    ("YYZ", "MBJ", "AC", 255),
    ("YYZ", "NAS", "AC", 205),
    ("YYZ", "PUJ", "AC", 260),
    ("YUL", "CUN", "AC", 285),
    ("YUL", "PUJ", "AC", 275),
    ("JFK", "AUA", "B6", 280),
    ("JFK", "CUN", "B6", 255),
    ("JFK", "MBJ", "B6", 240),
    ("JFK", "NAS", "B6", 190),
    ("JFK", "PUJ", "B6", 235),
    ("BOS", "CUN", "B6", 280),
    ("BOS", "NAS", "B6", 210),
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
    for origin, destination, airline, duration_min in ROUTES:
        if (origin, destination, airline) in existing:
            continue
        source, source_url = SOURCE[airline]
        payload["legs"].append({
            "origin": origin,
            "destination": destination,
            "airline": airline,
            "duration_min": duration_min,
            "confidence": "official_source_candidate",
            "source_tier": "A",
            "source": source,
            "source_url": source_url,
            "verified_at": "",
            "route_confidence": "medium",
        })
        existing.add((origin, destination, airline))
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
