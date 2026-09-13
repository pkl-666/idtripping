#!/usr/bin/env python3
"""Add the next practical batch of missing eligible airlines."""

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
    "AS": ("official Alaska Airlines destinations page", "https://www.alaskaair.com/en/?INT=sitemap-prodID%3ADestinations"),
    "BF": ("official French bee destinations page", "https://www.frenchbee.com/en/destinations"),
    "FJ": ("official Fiji Airways route network", "https://www.fijiairways.com/en-us/where-we-fly"),
    "JQ": ("official Jetstar route map", "https://www.jetstar.com/au/en/where-we-go/route-map"),
    "JX": ("official STARLUX Airlines destinations page", "https://www.starlux-airlines.com/en-US/route-map"),
    "NT": ("official Binter Canarias destinations page", "https://www.bintercanarias.com/eng/destinations"),
    "PD": ("official Porter Airlines where-we-fly page", "https://www.flyporter.com/en-us/book-flights/where-we-fly"),
    "PM": ("official Canaryfly destinations page", "https://www.canaryfly.es/en/destinations"),
    "QF": ("official Qantas where-we-fly page", "https://www.qantas.com/en-us/where-we-fly"),
    "TX": ("official Air Caraïbes destination maps", "https://www.aircaraibes.com/en/destination-maps"),
    "V7": ("official Volotea destinations page", "https://www.volotea.com/en/destinations/"),
    "VA": ("official Virgin Australia destinations page", "https://www.virginaustralia.com/au/en/destinations/all/"),
    "VB": ("official Viva Aerobus destinations page", "https://www.vivaaerobus.com/en-us/destinations"),
    "WS": ("official WestJet route map", "https://www.westjet.com/en-ca/flights/route-map"),
    "X3": ("official TUI fly route network", "https://www.tuifly.com/en/destinations"),
}

DESTINATIONS = [
    ("ACE", "Lanzarote", "Spain", ["europe", "warm_europe", "beach", "island"]),
    ("ANC", "Anchorage", "United States", ["north_america", "city"]),
    ("BCI", "Barcaldine", "Australia", ["oceania", "australia"]),
    ("BDA", "Bermuda", "Bermuda", ["caribbean", "beach", "island", "warm"]),
    ("BZE", "Belize City", "Belize", ["latin_america", "caribbean", "beach", "warm"]),
    ("CAY", "Cayenne", "French Guiana", ["south_america", "latin_america", "warm"]),
    ("CNS", "Cairns", "Australia", ["oceania", "australia", "beach", "warm"]),
    ("DAR", "Dar es Salaam", "Tanzania", ["africa", "city", "warm"]),
    ("DUB", "Dublin", "Ireland", ["europe", "city"]),
    ("EDI", "Edinburgh", "United Kingdom", ["europe", "city"]),
    ("FAE", "Faroe Islands", "Faroe Islands", ["europe", "nordic", "island"]),
    ("FDF", "Fort-de-France", "Martinique", ["caribbean", "beach", "island", "warm"]),
    ("FUE", "Fuerteventura", "Spain", ["europe", "warm_europe", "beach", "island"]),
    ("GCI", "Guernsey", "Guernsey", ["europe", "island"]),
    ("GOH", "Nuuk", "Greenland", ["nordic", "island"]),
    ("GUA", "Guatemala City", "Guatemala", ["latin_america", "city", "warm"]),
    ("HAV", "Havana", "Cuba", ["caribbean", "city", "warm"]),
    ("HNL", "Honolulu", "United States", ["north_america", "oceania", "beach", "island", "warm"]),
    ("JER", "Jersey", "Jersey", ["europe", "island"]),
    ("JRO", "Kilimanjaro", "Tanzania", ["africa", "warm"]),
    ("LAS", "Las Vegas", "United States", ["north_america", "city", "warm"]),
    ("LAX", "Los Angeles", "United States", ["north_america", "city", "warm"]),
    ("LUX", "Luxembourg", "Luxembourg", ["europe", "city"]),
    ("MCO", "Orlando", "United States", ["north_america", "city", "warm"]),
    ("MPL", "Montpellier", "France", ["europe", "warm_europe", "city"]),
    ("MSP", "Minneapolis", "United States", ["north_america", "city"]),
    ("NBO", "Nairobi", "Kenya", ["africa", "city", "warm"]),
    ("NOU", "Nouméa", "New Caledonia", ["oceania", "beach", "island", "warm"]),
    ("OAK", "Oakland", "United States", ["north_america", "city"]),
    ("OGG", "Maui", "United States", ["north_america", "oceania", "beach", "island", "warm"]),
    ("OPO", "Porto", "Portugal", ["europe", "warm_europe", "city"]),
    ("PAP", "Port-au-Prince", "Haiti", ["caribbean", "city", "warm"]),
    ("PFO", "Paphos", "Cyprus", ["europe", "warm_europe", "beach"]),
    ("PPT", "Papeete", "French Polynesia", ["oceania", "beach", "island", "warm"]),
    ("PTP", "Pointe-à-Pitre", "Guadeloupe", ["caribbean", "beach", "island", "warm"]),
    ("PVR", "Puerto Vallarta", "Mexico", ["latin_america", "beach", "warm"]),
    ("RAR", "Rarotonga", "Cook Islands", ["oceania", "beach", "island", "warm"]),
    ("RUN", "Réunion", "Réunion", ["indian_ocean", "beach", "island", "warm"]),
    ("SAN", "San Diego", "United States", ["north_america", "beach", "warm"]),
    ("SJD", "Los Cabos", "Mexico", ["latin_america", "beach", "warm"]),
    ("SJO", "San José", "Costa Rica", ["latin_america", "city", "warm"]),
    ("SNA", "Orange County", "United States", ["north_america", "beach", "warm"]),
    ("SXM", "Saint Martin", "Sint Maarten", ["caribbean", "beach", "island", "warm"]),
    ("TLS", "Toulouse", "France", ["europe", "city"]),
    ("TFN", "Tenerife North", "Spain", ["europe", "warm_europe", "beach", "island"]),
    ("VCE", "Venice", "Italy", ["europe", "warm_europe", "city"]),
    ("VIE", "Vienna", "Austria", ["europe", "city"]),
    ("WLG", "Wellington", "New Zealand", ["oceania", "city", "island"]),
    ("YOW", "Ottawa", "Canada", ["north_america", "city"]),
    ("YQB", "Quebec City", "Canada", ["north_america", "city"]),
    ("YVR", "Vancouver", "Canada", ["north_america", "city"]),
    ("YXE", "Saskatoon", "Canada", ["north_america", "city"]),
    ("YYC", "Calgary", "Canada", ["north_america", "city"]),
    ("YWG", "Winnipeg", "Canada", ["north_america", "city"]),
]

ROUTES = [
    # Alaska: useful North America / Pacific links from partner gateways.
    ("LAX", "ANC", "AS", 330),
    ("LAX", "CUN", "AS", 270),
    ("LAX", "GDL", "AS", 190),
    ("LAX", "HNL", "AS", 360),
    ("LAX", "LAS", "AS", 75),
    ("LAX", "LHR", "AS", 630),
    ("LAX", "NRT", "AS", 690),
    ("LAX", "OAK", "AS", 85),
    ("LAX", "PVR", "AS", 185),
    ("LAX", "SAN", "AS", 55),
    ("LAX", "SEA", "AS", 175),
    ("LAX", "SFO", "AS", 85),
    ("LAX", "SJD", "AS", 150),
    ("LAX", "SNA", "AS", 55),
    ("SEA", "ANC", "AS", 220),
    ("SEA", "HNL", "AS", 370),
    ("SEA", "JFK", "AS", 320),
    ("SEA", "LAX", "AS", 175),
    ("SEA", "NRT", "AS", 620),
    ("SEA", "SFO", "AS", 130),
    ("SEA", "SJO", "AS", 430),
    ("SEA", "YVR", "AS", 60),
    ("SFO", "HNL", "AS", 335),
    ("SFO", "JFK", "AS", 330),
    # WestJet / Porter: Canadian bridges and sun routes.
    ("CDG", "YYC", "WS", 540),
    ("DUB", "YYC", "WS", 480),
    ("EDI", "YYC", "WS", 465),
    ("LHR", "YYC", "WS", 535),
    ("YYC", "CUN", "WS", 330),
    ("YYC", "LAX", "WS", 195),
    ("YYC", "LAS", "WS", 160),
    ("YYC", "PVR", "WS", 285),
    ("YYC", "SJD", "WS", 265),
    ("YYC", "YVR", "WS", 95),
    ("YYC", "YYZ", "WS", 235),
    ("YVR", "CUN", "WS", 365),
    ("YVR", "HNL", "WS", 365),
    ("YVR", "LAX", "WS", 175),
    ("YVR", "YYZ", "WS", 270),
    ("YYZ", "CUN", "WS", 250),
    ("YYZ", "DUB", "WS", 400),
    ("YYZ", "LAS", "WS", 285),
    ("YYZ", "YUL", "WS", 80),
    ("YUL", "YVR", "PD", 330),
    ("YUL", "YYZ", "PD", 80),
    ("YYZ", "BOS", "PD", 95),
    ("YYZ", "CUN", "PD", 250),
    ("YYZ", "EWR", "PD", 95),
    ("YYZ", "FLL", "PD", 190),
    ("YYZ", "LAS", "PD", 285),
    ("YYZ", "LAX", "PD", 320),
    ("YYZ", "MCO", "PD", 180),
    ("YYZ", "MIA", "PD", 195),
    ("YYZ", "NAS", "PD", 205),
    ("YYZ", "YOW", "PD", 65),
    ("YYZ", "YQB", "PD", 95),
    ("YYZ", "YVR", "PD", 330),
    # French bee / Air Caraibes: French long-haul leisure.
    ("ORY", "EWR", "BF", 500),
    ("ORY", "LAX", "BF", 690),
    ("ORY", "MIA", "BF", 610),
    ("ORY", "PPT", "BF", 1320),
    ("ORY", "RUN", "BF", 660),
    ("ORY", "SFO", "BF", 690),
    ("SFO", "PPT", "BF", 490),
    ("ORY", "CAY", "TX", 545),
    ("ORY", "CUN", "TX", 610),
    ("ORY", "FDF", "TX", 515),
    ("ORY", "PAP", "TX", 560),
    ("ORY", "PTP", "TX", 515),
    ("ORY", "PUJ", "TX", 555),
    ("ORY", "RUN", "TX", 660),
    ("ORY", "SXM", "TX", 520),
    # STARLUX, Fiji and more Pacific.
    ("LAX", "TPE", "JX", 830),
    ("SFO", "TPE", "JX", 820),
    ("SEA", "TPE", "JX", 760),
    ("TPE", "BKK", "JX", 230),
    ("TPE", "CNS", "JX", 450),
    ("TPE", "DPS", "JX", 330),
    ("TPE", "HKG", "JX", 110),
    ("TPE", "KIX", "JX", 160),
    ("TPE", "NRT", "JX", 190),
    ("TPE", "SGN", "JX", 210),
    ("LAX", "NAN", "FJ", 660),
    ("SFO", "NAN", "FJ", 650),
    ("YVR", "NAN", "FJ", 685),
    ("NAN", "AKL", "FJ", 185),
    ("NAN", "HNL", "FJ", 380),
    ("NAN", "LAX", "FJ", 660),
    ("NAN", "MEL", "FJ", 310),
    ("NAN", "NRT", "FJ", 540),
    ("NAN", "SYD", "FJ", 235),
    # More Australia/New Zealand domestic/regional depth.
    ("SYD", "CNS", "QF", 185),
    ("SYD", "HNL", "QF", 590),
    ("SYD", "LAX", "QF", 815),
    ("SYD", "NOU", "QF", 175),
    ("SYD", "OOL", "QF", 80),
    ("SYD", "WLG", "QF", 190),
    ("BNE", "CNS", "VA", 135),
    ("BNE", "HNL", "JQ", 555),
    ("BNE", "OOL", "VA", 65),
    ("MEL", "AKL", "JQ", 215),
    ("MEL", "CNS", "JQ", 200),
    ("MEL", "OOL", "JQ", 125),
    ("MEL", "WLG", "JQ", 215),
    ("SYD", "AKL", "JQ", 190),
    ("SYD", "CNS", "JQ", 185),
    ("SYD", "HNL", "JQ", 590),
    ("SYD", "WLG", "JQ", 190),
    # Canary Islands and European leisure.
    ("LPA", "ACE", "NT", 45),
    ("LPA", "FUE", "NT", 40),
    ("LPA", "TFN", "NT", 35),
    ("TFN", "ACE", "NT", 50),
    ("TFN", "FUE", "NT", 50),
    ("TFN", "LPA", "NT", 35),
    ("LPA", "ACE", "PM", 45),
    ("LPA", "FUE", "PM", 40),
    ("LPA", "TFN", "PM", 35),
    ("TFN", "LPA", "PM", 35),
    ("ORY", "ACE", "V7", 225),
    ("ORY", "AGP", "V7", 155),
    ("ORY", "ALC", "V7", 130),
    ("ORY", "BIA", "V7", 100),
    ("ORY", "CUN", "V7", 610),
    ("ORY", "FAO", "V7", 155),
    ("ORY", "MPL", "V7", 85),
    ("ORY", "NAP", "V7", 135),
    ("ORY", "OPO", "V7", 135),
    ("ORY", "PMI", "V7", 115),
    ("ORY", "TLS", "V7", 80),
    ("ORY", "VCE", "V7", 105),
    ("DUS", "AGP", "X3", 185),
    ("DUS", "AYT", "X3", 220),
    ("DUS", "FUE", "X3", 280),
    ("DUS", "HER", "X3", 205),
    ("DUS", "LPA", "X3", 285),
    ("DUS", "PMI", "X3", 140),
    ("DUS", "TFS", "X3", 290),
    ("FRA", "AGP", "X3", 180),
    ("FRA", "FUE", "X3", 280),
    ("FRA", "HER", "X3", 200),
    ("FRA", "LPA", "X3", 285),
    ("FRA", "PMI", "X3", 125),
    ("FRA", "TFS", "X3", 290),
    # Viva Aerobus / Mexico.
    ("MEX", "CUN", "VB", 135),
    ("MEX", "GDL", "VB", 80),
    ("MEX", "LAX", "VB", 240),
    ("MEX", "LAS", "VB", 240),
    ("MEX", "PVR", "VB", 100),
    ("MEX", "SJD", "VB", 130),
    ("MEX", "SJO", "VB", 180),
    ("CUN", "BOG", "VB", 205),
    ("CUN", "GDL", "VB", 190),
    ("CUN", "MIA", "VB", 105),
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
