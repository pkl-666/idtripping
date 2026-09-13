#!/usr/bin/env python3
"""Add more eligible airlines, hubs, and long-haul ideas to the route prototype."""

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

SOURCES = {
    "AC": ("official Air Canada where-we-fly page", "https://www.aircanada.com/us/en/aco/home/book/routes-and-partners/where-we-fly.html"),
    "AA": ("official American Airlines route map", "https://www.aa.com/travelInformation/flights/routeMap"),
    "AI": ("official Air India route map", "https://www.airindia.com/in/en/book/routes-and-schedules.html"),
    "DL": ("official Delta route map", "https://www.delta.com/us/en/flight-deals/current-flight-deals/route-map"),
    "EW": ("official Eurowings flight routes page", "https://www.eurowings.com/content/eurowings/en/discover/destinations/flight-routes.html"),
    "EY": ("official Etihad destination network", "https://www.etihad.com/en/fly-etihad/our-destinations"),
    "FI": ("official Icelandair network routemap", "https://www.icelandair.com/about/routemap/"),
    "LO": ("official LOT route map", "https://www.lot.com/is/en/explore/inspirations/route-map"),
    "LX": ("official SWISS destinations page", "https://www.swiss.com/lhg/ch/en/o-d/cy-cy"),
    "OS": ("official Austrian route map", "https://www.austrian.com/us/en/route-map"),
    "SN": ("official Brussels Airlines destinations page", "https://www.brusselsairlines.com/br/en/book-a-flight/our-destinations"),
    "UA": ("official United destination map", "https://www.united.com/en/us/destination-map/"),
}

DESTINATIONS = [
    ("AUH", "Abu Dhabi", "United Arab Emirates", ["asia", "middle_east", "city", "warm"]),
    ("BKK", "Bangkok", "Thailand", ["asia", "city", "warm"]),
    ("BOM", "Mumbai", "India", ["asia", "city", "warm"]),
    ("BOS", "Boston", "United States", ["north_america", "city"]),
    ("BRU", "Brussels", "Belgium", ["europe", "city"]),
    ("DEL", "Delhi", "India", ["asia", "city", "warm"]),
    ("DUS", "Düsseldorf", "Germany", ["europe", "city"]),
    ("EWR", "Newark / New York", "United States", ["north_america", "city"]),
    ("HAM", "Hamburg", "Germany", ["europe", "city"]),
    ("IAD", "Washington Dulles", "United States", ["north_america", "city"]),
    ("ICN", "Seoul", "South Korea", ["asia", "city"]),
    ("JFK", "New York JFK", "United States", ["north_america", "city"]),
    ("KEF", "Reykjavik Keflavik", "Iceland", ["europe", "nordic", "island"]),
    ("LAX", "Los Angeles", "United States", ["north_america", "city", "warm"]),
    ("MIA", "Miami", "United States", ["north_america", "beach", "warm"]),
    ("ORD", "Chicago", "United States", ["north_america", "city"]),
    ("SEA", "Seattle", "United States", ["north_america", "city"]),
    ("SFO", "San Francisco", "United States", ["north_america", "city"]),
    ("VIE", "Vienna", "Austria", ["europe", "city"]),
    ("WAW", "Warsaw", "Poland", ["europe", "city"]),
    ("YUL", "Montreal", "Canada", ["north_america", "city"]),
    ("YYZ", "Toronto", "Canada", ["north_america", "city"]),
    ("ZRH", "Zurich", "Switzerland", ["europe", "city"]),
]

ROUTES = [
    # Wideroe domestic backbone from Bergen.
    ("BGO", "AES", "WF", 50, "official Widerøe route map", "https://www.wideroe.no/en/travel-information/route-map", "medium"),
    ("BGO", "BOO", "WF", 115, "official Widerøe route map", "https://www.wideroe.no/en/travel-information/route-map", "medium"),
    ("BGO", "SVG", "WF", 40, "official Widerøe route map", "https://www.wideroe.no/en/travel-information/route-map", "medium"),
    ("BGO", "TRD", "WF", 65, "official Widerøe route map", "https://www.wideroe.no/en/travel-information/route-map", "medium"),
    ("BGO", "TOS", "WF", 125, "official Widerøe route map", "https://www.wideroe.no/en/travel-information/route-map", "medium"),
    # Icelandair: Scandinavia/Europe to KEF and useful onward ideas.
    ("OSL", "KEF", "FI", 175),
    ("BGO", "KEF", "FI", 155),
    ("KEF", "AGP", "FI", 293),
    ("KEF", "ALC", "FI", 288),
    ("KEF", "BCN", "FI", 269),
    ("KEF", "BOS", "FI", 335),
    ("KEF", "EWR", "FI", 362),
    ("KEF", "FCO", "FI", 295),
    ("KEF", "IAD", "FI", 386),
    ("KEF", "JFK", "FI", 360),
    ("KEF", "LIS", "FI", 266),
    ("KEF", "LPA", "FI", 353),
    ("KEF", "NCE", "FI", 255),
    ("KEF", "ORD", "FI", 407),
    ("KEF", "SEA", "FI", 489),
    ("KEF", "TFS", "FI", 351),
    ("KEF", "YYZ", "FI", 360),
    # SWISS via Zurich.
    ("OSL", "ZRH", "LX", 150),
    ("ZRH", "AGP", "LX", 165),
    ("ZRH", "ATH", "LX", 160),
    ("ZRH", "BCN", "LX", 105),
    ("ZRH", "DXB", "LX", 380),
    ("ZRH", "FCO", "LX", 95),
    ("ZRH", "LCA", "LX", 215),
    ("ZRH", "LIS", "LX", 175),
    ("ZRH", "MAD", "LX", 145),
    ("ZRH", "NCE", "LX", 70),
    ("ZRH", "PMI", "LX", 115),
    # Austrian via Vienna.
    ("OSL", "VIE", "OS", 140),
    ("VIE", "AGP", "OS", 195),
    ("VIE", "ATH", "OS", 135),
    ("VIE", "BCN", "OS", 150),
    ("VIE", "FCO", "OS", 90),
    ("VIE", "LCA", "OS", 180),
    ("VIE", "NCE", "OS", 105),
    ("VIE", "PMI", "OS", 145),
    # Brussels Airlines via Brussels.
    ("OSL", "BRU", "SN", 120),
    ("BGO", "BRU", "SN", 120),
    ("BRU", "AGP", "SN", 170),
    ("BRU", "ALC", "SN", 155),
    ("BRU", "ATH", "SN", 190),
    ("BRU", "BCN", "SN", 125),
    ("BRU", "FCO", "SN", 125),
    ("BRU", "LIS", "SN", 165),
    ("BRU", "MAD", "SN", 140),
    ("BRU", "NCE", "SN", 105),
    # LOT via Warsaw.
    ("OSL", "WAW", "LO", 115),
    ("BGO", "WAW", "LO", 130),
    ("WAW", "AGP", "LO", 245),
    ("WAW", "ATH", "LO", 160),
    ("WAW", "BCN", "LO", 185),
    ("WAW", "DEL", "LO", 405),
    ("WAW", "DXB", "LO", 355),
    ("WAW", "FCO", "LO", 140),
    ("WAW", "ICN", "LO", 655),
    ("WAW", "IST", "LO", 160),
    ("WAW", "LCA", "LO", 200),
    ("WAW", "MAD", "LO", 220),
    ("WAW", "NCE", "LO", 150),
    ("WAW", "PMI", "LO", 190),
    # Eurowings via Dusseldorf.
    ("OSL", "DUS", "EW", 110),
    ("DUS", "AGP", "EW", 185),
    ("DUS", "ATH", "EW", 185),
    ("DUS", "BCN", "EW", 135),
    ("DUS", "FCO", "EW", 120),
    ("DUS", "NCE", "EW", 105),
    ("DUS", "PMI", "EW", 140),
    # North America via existing European hubs.
    ("FRA", "YYZ", "AC", 500),
    ("LHR", "YYZ", "AC", 475),
    ("CDG", "YUL", "AC", 455),
    ("FRA", "EWR", "UA", 520),
    ("FRA", "IAD", "UA", 535),
    ("LHR", "EWR", "UA", 480),
    ("LHR", "ORD", "UA", 535),
    ("CDG", "JFK", "DL", 500),
    ("AMS", "BOS", "DL", 470),
    ("AMS", "JFK", "DL", 500),
    ("LHR", "JFK", "AA", 480),
    ("LHR", "MIA", "AA", 580),
    ("LHR", "ORD", "AA", 535),
    # India / Gulf ideas from hubs already reachable.
    ("CPH", "AUH", "EY", 385),
    ("ARN", "AUH", "EY", 395),
    ("AUH", "BKK", "EY", 390),
    ("AUH", "BOM", "EY", 190),
    ("AUH", "DEL", "EY", 200),
    ("AUH", "MLE", "EY", 260),
    ("FRA", "DEL", "AI", 460),
    ("LHR", "DEL", "AI", 510),
    ("CDG", "DEL", "AI", 500),
]

EXTRA_NORWAY_DESTINATIONS = [
    ("AES", "Ålesund", "Norway", ["europe", "nordic", "city"]),
    ("BOO", "Bodø", "Norway", ["europe", "nordic", "city"]),
    ("SVG", "Stavanger", "Norway", ["europe", "nordic", "city"]),
    ("TRD", "Trondheim", "Norway", ["europe", "nordic", "city"]),
    ("TOS", "Tromsø", "Norway", ["europe", "nordic", "city"]),
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
    for iata, city, country, regions in [*DESTINATIONS, *EXTRA_NORWAY_DESTINATIONS]:
        if iata in existing:
            continue
        payload["destinations"].append({
            "iata": iata,
            "city": city,
            "country": country,
            "regions": regions,
        })
        existing.add(iata)
        added += 1
    payload["updated_at"] = TODAY
    save_json(DESTINATIONS_PATH, payload)
    save_json(APP_DESTINATIONS_PATH, payload)
    return added


def route_payload(origin: str, destination: str, airline: str, duration_min: int, source: str | None = None, url: str | None = None, confidence: str = "medium") -> dict[str, Any]:
    default_source, default_url = SOURCES.get(airline, ("starter curated route map", ""))
    return {
        "origin": origin,
        "destination": destination,
        "airline": airline,
        "duration_min": duration_min,
        "confidence": "official_source_candidate",
        "source_tier": "A" if (url or default_url) else "C",
        "source": source or default_source,
        "source_url": url or default_url,
        "verified_at": "",
        "route_confidence": confidence,
    }


def add_routes() -> int:
    payload = load_json(ROUTES_PATH)
    existing = {(item["origin"], item["destination"], item["airline"]) for item in payload["legs"]}
    added = 0
    for row in ROUTES:
        origin, destination, airline, duration_min, *rest = row
        source = rest[0] if len(rest) >= 1 else None
        url = rest[1] if len(rest) >= 2 else None
        confidence = rest[2] if len(rest) >= 3 else "medium"
        key = (origin, destination, airline)
        if key in existing:
            continue
        payload["legs"].append(route_payload(origin, destination, airline, duration_min, source, url, confidence))
        existing.add(key)
        added += 1
    payload["updated_at"] = TODAY
    save_json(ROUTES_PATH, payload)
    save_json(APP_ROUTES_PATH, payload)
    return added


def main() -> int:
    destinations_added = add_destinations()
    routes_added = add_routes()
    print(f"Added {destinations_added} destination(s).")
    print(f"Added {routes_added} route leg(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
