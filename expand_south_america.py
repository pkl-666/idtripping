#!/usr/bin/env python3
"""Add South America / Latin America route ideas for eligible airlines."""

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
    "AF": ("official Air France destinations page", "https://wwws.airfrance.co.uk/en-gb/"),
    "BA": ("official British Airways route network", "https://www.britishairways.com/content/en/kw/information/flight-information/our-route-network"),
    "IB": ("official Iberia South America destinations page", "https://grupo.iberia.es/about_us/destinations/south-america"),
    "LA": ("official LATAM destination network", "https://latamairlines.gcs-web.com/pt-pt/network"),
    "TP": ("official TAP destinations page", "https://www.flytap.com/en-ar/destinations"),
    "UX": ("official Air Europa destinations page", "https://www.aireuropa.com/ot/en/aea/aexperience/our-destinations.html"),
}

DESTINATIONS = [
    ("ASU", "Asunción", "Paraguay", ["south_america", "latin_america", "city", "warm"]),
    ("BEL", "Belém", "Brazil", ["south_america", "latin_america", "city", "warm"]),
    ("BOG", "Bogotá", "Colombia", ["south_america", "latin_america", "city"]),
    ("BSB", "Brasília", "Brazil", ["south_america", "latin_america", "city", "warm"]),
    ("CNF", "Belo Horizonte", "Brazil", ["south_america", "latin_america", "city", "warm"]),
    ("COR", "Córdoba", "Argentina", ["south_america", "latin_america", "city"]),
    ("CTG", "Cartagena", "Colombia", ["south_america", "latin_america", "caribbean", "beach", "warm"]),
    ("CWB", "Curitiba", "Brazil", ["south_america", "latin_america", "city"]),
    ("EZE", "Buenos Aires Ezeiza", "Argentina", ["south_america", "latin_america", "city"]),
    ("FOR", "Fortaleza", "Brazil", ["south_america", "latin_america", "beach", "warm"]),
    ("GIG", "Rio de Janeiro", "Brazil", ["south_america", "latin_america", "city", "beach", "warm"]),
    ("GRU", "São Paulo Guarulhos", "Brazil", ["south_america", "latin_america", "city"]),
    ("GYE", "Guayaquil", "Ecuador", ["south_america", "latin_america", "city", "warm"]),
    ("LIM", "Lima", "Peru", ["south_america", "latin_america", "city"]),
    ("MAO", "Manaus", "Brazil", ["south_america", "latin_america", "city", "warm"]),
    ("MDE", "Medellín", "Colombia", ["south_america", "latin_america", "city", "warm"]),
    ("MVD", "Montevideo", "Uruguay", ["south_america", "latin_america", "city"]),
    ("POA", "Porto Alegre", "Brazil", ["south_america", "latin_america", "city"]),
    ("REC", "Recife", "Brazil", ["south_america", "latin_america", "beach", "warm"]),
    ("SCL", "Santiago de Chile", "Chile", ["south_america", "latin_america", "city"]),
    ("SSA", "Salvador", "Brazil", ["south_america", "latin_america", "beach", "warm"]),
    ("UIO", "Quito", "Ecuador", ["south_america", "latin_america", "city"]),
    ("VVI", "Santa Cruz de la Sierra", "Bolivia", ["south_america", "latin_america", "city", "warm"]),
]

ROUTES = [
    # Iberia / Air Europa: Madrid as the strongest Spain-Latin America gateway.
    ("MAD", "ASU", "UX", 670),
    ("MAD", "BOG", "IB", 635),
    ("MAD", "BOG", "UX", 635),
    ("MAD", "COR", "UX", 775),
    ("MAD", "EZE", "IB", 780),
    ("MAD", "EZE", "UX", 780),
    ("MAD", "GIG", "IB", 620),
    ("MAD", "GRU", "IB", 640),
    ("MAD", "GRU", "LA", 640),
    ("MAD", "GRU", "UX", 640),
    ("MAD", "GYE", "IB", 680),
    ("MAD", "GYE", "UX", 680),
    ("MAD", "LIM", "IB", 720),
    ("MAD", "LIM", "LA", 720),
    ("MAD", "MVD", "IB", 765),
    ("MAD", "MVD", "UX", 765),
    ("MAD", "SCL", "IB", 805),
    ("MAD", "SCL", "LA", 805),
    ("MAD", "UIO", "IB", 675),
    ("MAD", "VVI", "UX", 700),
    # TAP: Lisbon to Brazil.
    ("LIS", "BEL", "TP", 455),
    ("LIS", "BSB", "TP", 570),
    ("LIS", "CNF", "TP", 590),
    ("LIS", "FOR", "TP", 440),
    ("LIS", "GIG", "TP", 595),
    ("LIS", "GRU", "TP", 610),
    ("LIS", "MAO", "TP", 565),
    ("LIS", "REC", "TP", 455),
    ("LIS", "SSA", "TP", 510),
    # Air France / British Airways transatlantic gateways.
    ("CDG", "BOG", "AF", 660),
    ("CDG", "EZE", "AF", 820),
    ("CDG", "GIG", "AF", 700),
    ("CDG", "GRU", "AF", 715),
    ("CDG", "LIM", "AF", 740),
    ("CDG", "SCL", "AF", 860),
    ("LHR", "EZE", "BA", 820),
    ("LHR", "GIG", "BA", 700),
    ("LHR", "GRU", "BA", 715),
    ("LHR", "SCL", "BA", 870),
    # Miami / North America as useful one-stop or two-stop bridges.
    ("MIA", "BOG", "AA", 225),
    ("MIA", "BOG", "LA", 225),
    ("MIA", "EZE", "AA", 540),
    ("MIA", "GIG", "AA", 500),
    ("MIA", "GRU", "AA", 510),
    ("MIA", "GRU", "LA", 510),
    ("MIA", "LIM", "AA", 355),
    ("MIA", "LIM", "LA", 355),
    ("MIA", "SCL", "AA", 500),
    ("MIA", "SCL", "LA", 500),
    ("JFK", "GRU", "LA", 575),
    ("JFK", "SCL", "LA", 640),
    # LATAM regional backbone for onward ideas.
    ("BOG", "CTG", "LA", 90),
    ("BOG", "MDE", "LA", 60),
    ("GRU", "BSB", "LA", 105),
    ("GRU", "CNF", "LA", 75),
    ("GRU", "CWB", "LA", 70),
    ("GRU", "FOR", "LA", 210),
    ("GRU", "GIG", "LA", 65),
    ("GRU", "LIM", "LA", 315),
    ("GRU", "POA", "LA", 105),
    ("GRU", "REC", "LA", 180),
    ("GRU", "SCL", "LA", 245),
    ("GRU", "SSA", "LA", 145),
    ("LIM", "BOG", "LA", 190),
    ("LIM", "GYE", "LA", 125),
    ("LIM", "SCL", "LA", 215),
    ("LIM", "UIO", "LA", 135),
    ("SCL", "EZE", "LA", 125),
    ("SCL", "LIM", "LA", 215),
    ("SCL", "MVD", "LA", 140),
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
        key = (origin, destination, airline)
        if key in existing:
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
