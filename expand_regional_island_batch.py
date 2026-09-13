#!/usr/bin/env python3
"""Add regional, island, Nordic, Atlantic and Pacific eligible airlines."""

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
    "3B": ("official Cabo Verde airport destinations page", "https://www.caboverde-airports.cv/destinos/"),
    "GL": ("official Air Greenland route network", "https://airgreenland.com/about-us/routes-our-network/"),
    "GZ": ("official Air Rarotonga destinations page", "https://www.airraro.com/en/destinations"),
    "LG": ("Luxair route map reference", "https://www.flightconnections.com/route-map-luxair-lg"),
    "LM": ("official Loganair route map", "https://www.loganair.co.uk/destinations/route-map/"),
    "LY": ("official EL AL route map", "https://www.elal.com/eng/route-map"),
    "OU": ("official Croatia Airlines destinations page", "https://www.croatiaairlines.com/se/destinationer"),
    "PX": ("official Air Niugini route maps", "https://www.airniugini.com.pg/en-pg/plan/route-maps/"),
    "QS": ("official Smartwings flight schedule", "https://www.smartwings.com/en/flight-schedule"),
    "RC": ("official Atlantic Airways route map", "https://www.atlanticairways.com/en/"),
    "S4": ("official Azores Airlines destinations page", "https://sata4agents.azoresairlines.pt/pt-pt/sobre-sata/destinos"),
    "SB": ("official Aircalin destinations page", "https://www.aircalin.com/en/destinations"),
    "SP": ("official SATA Air Açores airport destination page", "https://www.santamariaairport.pt/en/sma/flights-destinations/airlines/airlines-and-destinations"),
    "TY": ("official Air Calédonie destinations page", "https://www.air-caledonie.nc/en/destinations"),
    "UU": ("official Air Austral network page", "https://www.air-austral.com/en/where-we-fly/our-network.html"),
    "VR": ("official Cabo Verde Airlines destinations page", "https://www.caboverdeairlines.com/planear-e-reservar/destinos?format=html"),
    "WK": ("official Edelweiss destinations page", "https://www.flyedelweiss.com/ch/en/destinations.html"),
}

DESTINATIONS = [
    ("AAL", "Aalborg", "Denmark", ["europe", "nordic", "city"]),
    ("ABZ", "Aberdeen", "United Kingdom", ["europe", "city"]),
    ("AIT", "Aitutaki", "Cook Islands", ["oceania", "beach", "island", "warm"]),
    ("BIL", "Billund", "Denmark", ["europe", "nordic", "city"]),
    ("BVC", "Boa Vista", "Cape Verde", ["africa", "beach", "island", "warm"]),
    ("BWK", "Brač", "Croatia", ["europe", "warm_europe", "beach", "island"]),
    ("DBV", "Dubrovnik", "Croatia", ["europe", "warm_europe", "beach", "city"]),
    ("DND", "Dundee", "United Kingdom", ["europe", "city"]),
    ("DZA", "Dzaoudzi", "Mayotte", ["indian_ocean", "africa", "beach", "island", "warm"]),
    ("GCM", "Grand Cayman", "Cayman Islands", ["caribbean", "beach", "island", "warm"]),
    ("GEA", "Nouméa Magenta", "New Caledonia", ["oceania", "island", "warm"]),
    ("HOR", "Horta", "Portugal", ["azores", "europe", "island"]),
    ("INV", "Inverness", "United Kingdom", ["europe", "city"]),
    ("IOM", "Isle of Man", "Isle of Man", ["europe", "island"]),
    ("JAV", "Ilulissat", "Greenland", ["nordic", "greenland", "island"]),
    ("JCI", "Kansas City", "United States", ["north_america", "city"]),
    ("JEG", "Aasiaat", "Greenland", ["nordic", "greenland", "island"]),
    ("KGI", "Kalgoorlie", "Australia", ["oceania", "australia"]),
    ("KOI", "Kirkwall", "United Kingdom", ["europe", "island"]),
    ("KUS", "Kulusuk", "Greenland", ["nordic", "greenland", "island"]),
    ("LIF", "Lifou", "New Caledonia", ["oceania", "beach", "island", "warm"]),
    ("LSI", "Shetland", "United Kingdom", ["europe", "island"]),
    ("MJN", "Mahajanga", "Madagascar", ["indian_ocean", "africa", "beach", "warm"]),
    ("POM", "Port Moresby", "Papua New Guinea", ["oceania", "city", "warm"]),
    ("PDL", "Ponta Delgada", "Portugal", ["azores", "europe", "island"]),
    ("PRG", "Prague", "Czechia", ["europe", "city"]),
    ("RAI", "Praia", "Cape Verde", ["africa", "beach", "island", "warm"]),
    ("SID", "Sal", "Cape Verde", ["africa", "beach", "island", "warm"]),
    ("SFJ", "Kangerlussuaq", "Greenland", ["nordic", "greenland", "island"]),
    ("SMA", "Santa Maria", "Portugal", ["azores", "europe", "island"]),
    ("SPU", "Split", "Croatia", ["europe", "warm_europe", "beach", "city"]),
    ("SYY", "Stornoway", "United Kingdom", ["europe", "island"]),
    ("TER", "Terceira", "Portugal", ["azores", "europe", "island"]),
    ("TLV", "Tel Aviv", "Israel", ["middle_east", "beach", "city", "warm"]),
    ("VXE", "São Vicente", "Cape Verde", ["africa", "beach", "island", "warm"]),
    ("ZAD", "Zadar", "Croatia", ["europe", "warm_europe", "beach", "city"]),
    ("ZAG", "Zagreb", "Croatia", ["europe", "city"]),
]

ROUTES = [
    # Greenland and Faroe Islands.
    ("CPH", "GOH", "GL", 270),
    ("CPH", "JAV", "GL", 285),
    ("CPH", "SFJ", "GL", 255),
    ("KEF", "GOH", "GL", 190),
    ("KEF", "KUS", "GL", 115),
    ("GOH", "JAV", "GL", 75),
    ("GOH", "SFJ", "GL", 55),
    ("GOH", "JEG", "GL", 80),
    ("SFJ", "JAV", "GL", 50),
    ("FAE", "BCN", "RC", 225),
    ("FAE", "CPH", "RC", 125),
    ("FAE", "EDI", "RC", 85),
    ("FAE", "KEF", "RC", 95),
    ("FAE", "LPA", "RC", 320),
    ("FAE", "OSL", "RC", 105),
    ("FAE", "PMI", "RC", 215),
    ("FAE", "TFS", "RC", 325),
    # UK regional.
    ("EDI", "DND", "LM", 45),
    ("EDI", "IOM", "LM", 60),
    ("EDI", "KOI", "LM", 70),
    ("EDI", "LSI", "LM", 85),
    ("EDI", "SYY", "LM", 70),
    ("LHR", "DND", "LM", 100),
    ("LHR", "IOM", "LM", 80),
    # Luxair / Croatia / Smartwings.
    ("LUX", "AGP", "LG", 155),
    ("LUX", "BCN", "LG", 115),
    ("LUX", "FCO", "LG", 110),
    ("LUX", "LPA", "LG", 260),
    ("LUX", "NCE", "LG", 90),
    ("LUX", "OPO", "LG", 150),
    ("LUX", "PMI", "LG", 125),
    ("LUX", "TFS", "LG", 265),
    ("FRA", "ZAG", "OU", 90),
    ("MUC", "ZAG", "OU", 75),
    ("ZAG", "DBV", "OU", 55),
    ("ZAG", "FCO", "OU", 80),
    ("ZAG", "SPU", "OU", 45),
    ("ZAG", "ZAD", "OU", 45),
    ("ZAG", "BWK", "OU", 45),
    ("BGO", "PRG", "QS", 130),
    ("PRG", "AGP", "QS", 205),
    ("PRG", "AYT", "QS", 170),
    ("PRG", "LPA", "QS", 300),
    ("PRG", "PMI", "QS", 150),
    ("PRG", "TFS", "QS", 305),
    ("PRG", "SPU", "QS", 90),
    # Azores / Cabo Verde.
    ("LIS", "PDL", "S4", 150),
    ("LIS", "TER", "S4", 160),
    ("OPO", "PDL", "S4", 145),
    ("BOS", "PDL", "S4", 300),
    ("JFK", "PDL", "S4", 335),
    ("PDL", "BOS", "S4", 300),
    ("PDL", "JFK", "S4", 335),
    ("PDL", "TER", "SP", 40),
    ("PDL", "HOR", "SP", 55),
    ("PDL", "SMA", "SP", 30),
    ("TER", "HOR", "SP", 35),
    ("TER", "SMA", "SP", 45),
    ("LIS", "RAI", "VR", 255),
    ("LIS", "SID", "VR", 250),
    ("OPO", "RAI", "VR", 260),
    ("CDG", "SID", "VR", 355),
    ("RAI", "SID", "VR", 45),
    ("RAI", "VXE", "VR", 55),
    ("SID", "BVC", "VR", 35),
    ("RAI", "BVC", "3B", 40),
    ("RAI", "SID", "3B", 45),
    ("SID", "BVC", "3B", 35),
    ("SID", "VXE", "3B", 50),
    # Indian Ocean / Pacific regional.
    ("CDG", "RUN", "UU", 660),
    ("RUN", "DZA", "UU", 135),
    ("RUN", "MRU", "UU", 45),
    ("RUN", "MJN", "UU", 105),
    ("RUN", "SEZ", "UU", 170),
    ("RUN", "JNB", "UU", 240),
    ("BNE", "POM", "PX", 190),
    ("CNS", "POM", "PX", 85),
    ("HKG", "POM", "PX", 390),
    ("MNL", "POM", "PX", 330),
    ("POM", "BNE", "PX", 190),
    ("POM", "CNS", "PX", 85),
    ("POM", "HKG", "PX", 390),
    ("POM", "SIN", "PX", 380),
    ("NOU", "BNE", "SB", 145),
    ("NOU", "NRT", "SB", 520),
    ("NOU", "PPT", "SB", 360),
    ("NOU", "SIN", "SB", 520),
    ("NOU", "SYD", "SB", 175),
    ("NOU", "AKL", "SB", 170),
    ("NOU", "GEA", "TY", 20),
    ("GEA", "LIF", "TY", 40),
    ("NOU", "LIF", "TY", 40),
    ("RAR", "AIT", "GZ", 50),
    # Edelweiss / EL AL for additional leisure and Israel.
    ("ZRH", "CPT", "WK", 700),
    ("ZRH", "HKT", "WK", 670),
    ("ZRH", "LPA", "WK", 270),
    ("ZRH", "MLE", "WK", 600),
    ("ZRH", "MRU", "WK", 690),
    ("ZRH", "SEZ", "WK", 610),
    ("ZRH", "TFS", "WK", 275),
    ("ATH", "TLV", "LY", 125),
    ("FCO", "TLV", "LY", 205),
    ("LHR", "TLV", "LY", 300),
    ("TLV", "BKK", "LY", 650),
    ("TLV", "DXB", "LY", 200),
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
