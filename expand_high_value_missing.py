#!/usr/bin/env python3
"""Add a high-value batch of missing eligible airlines."""

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
    "6E": ("official IndiGo destinations page", "https://www.goindigo.in/route-map.html"),
    "AD": ("official Azul destinations page", "https://www.voeazul.com.br/en/destinations"),
    "AF": ("official Air France destinations page", "https://wwws.airfrance.co.uk/en-gb/"),
    "AM": ("official Aeromexico route network", "https://aeromexico.com/en-us/routes"),
    "AR": ("official Aerolineas Argentinas destinations page", "https://www.aerolineas.com.ar/en-us/destinations"),
    "AV": ("official Avianca route network", "https://www.avianca.com/en/destinations/"),
    "AZ": ("official ITA Airways network page", "https://www.ita-airways.com/en_us/fly-ita/ita-world/network.html"),
    "BR": ("official EVA Air route map", "https://www.evaair.com/en-sg/plan-and-book/where-we-fly/route-maps/long-haul-route-map/"),
    "DE": ("official Condor route network", "https://www.condor.com/en-ca/explore/destinations/route-map/"),
    "FZ": ("official flydubai destinations page", "https://www.flydubai.com/en-us/destinations/"),
    "JQ": ("official Jetstar route map", "https://www.jetstar.com/au/en/where-we-go/route-map"),
    "QF": ("official Qantas where-we-fly page", "https://www.qantas.com/en-us/where-we-fly"),
    "TO": ("official Transavia France destinations page", "https://www.transavia.com/en-EU/destinations/"),
    "TS": ("official Air Transat destinations page", "https://www.airtransat.com/en-CA/destinations"),
    "UL": ("official SriLankan Airlines flight routes", "https://www.srilankan.com/si_lk/plan-and-book/flight-routes"),
    "VA": ("official Virgin Australia destinations page", "https://www.virginaustralia.com/au/en/destinations/all/"),
    "VY": ("official Vueling destinations page", "https://www.vueling.com/en/vueling-destinations"),
}

DESTINATIONS = [
    ("ALA", "Almaty", "Kazakhstan", ["asia", "city"]),
    ("AMM", "Amman", "Jordan", ["middle_east", "city", "warm"]),
    ("BIA", "Bastia", "France", ["europe", "warm_europe", "beach", "island"]),
    ("BJV", "Bodrum", "Türkiye", ["europe", "warm_europe", "beach"]),
    ("BLR", "Bengaluru", "India", ["asia", "city", "warm"]),
    ("CAI", "Cairo", "Egypt", ["africa", "middle_east", "city", "warm"]),
    ("CCS", "Caracas", "Venezuela", ["south_america", "latin_america", "city", "warm"]),
    ("CCU", "Kolkata", "India", ["asia", "city", "warm"]),
    ("CHC", "Christchurch", "New Zealand", ["oceania", "city", "island"]),
    ("COK", "Kochi", "India", ["asia", "beach", "warm"]),
    ("CPT", "Cape Town", "South Africa", ["africa", "city", "beach"]),
    ("CUN", "Cancun", "Mexico", ["caribbean", "latin_america", "beach", "warm"]),
    ("DAC", "Dhaka", "Bangladesh", ["asia", "city", "warm"]),
    ("DAD", "Da Nang", "Vietnam", ["asia", "beach", "warm"]),
    ("DPS", "Denpasar Bali", "Indonesia", ["asia", "beach", "island", "warm"]),
    ("FOR", "Fortaleza", "Brazil", ["south_america", "latin_america", "beach", "warm"]),
    ("FLL", "Fort Lauderdale", "United States", ["north_america", "beach", "warm"]),
    ("GDL", "Guadalajara", "Mexico", ["latin_america", "city", "warm"]),
    ("GYD", "Baku", "Azerbaijan", ["asia", "city"]),
    ("HAN", "Hanoi", "Vietnam", ["asia", "city", "warm"]),
    ("HKG", "Hong Kong", "Hong Kong", ["asia", "city", "warm"]),
    ("HYD", "Hyderabad", "India", ["asia", "city", "warm"]),
    ("JNB", "Johannesburg", "South Africa", ["africa", "city"]),
    ("KBV", "Krabi", "Thailand", ["asia", "beach", "warm"]),
    ("KHI", "Karachi", "Pakistan", ["asia", "city", "warm"]),
    ("KTM", "Kathmandu", "Nepal", ["asia", "city"]),
    ("LGK", "Langkawi", "Malaysia", ["asia", "beach", "island", "warm"]),
    ("MBA", "Mombasa", "Kenya", ["africa", "beach", "warm"]),
    ("MEX", "Mexico City", "Mexico", ["latin_america", "city"]),
    ("MRU", "Mauritius", "Mauritius", ["indian_ocean", "beach", "island", "warm"]),
    ("NAP", "Naples", "Italy", ["europe", "warm_europe", "city"]),
    ("OOL", "Gold Coast", "Australia", ["oceania", "australia", "beach", "warm"]),
    ("ORY", "Paris Orly", "France", ["europe", "city"]),
    ("PEN", "Penang", "Malaysia", ["asia", "beach", "warm"]),
    ("PNH", "Phnom Penh", "Cambodia", ["asia", "city", "warm"]),
    ("POP", "Puerto Plata", "Dominican Republic", ["caribbean", "beach", "warm"]),
    ("PVG", "Shanghai Pudong", "China", ["asia", "city"]),
    ("RAK", "Marrakesh", "Morocco", ["africa", "warm", "city"]),
    ("SDQ", "Santo Domingo", "Dominican Republic", ["caribbean", "city", "warm"]),
    ("SGN", "Ho Chi Minh City", "Vietnam", ["asia", "city", "warm"]),
    ("TAS", "Tashkent", "Uzbekistan", ["asia", "city"]),
    ("TBS", "Tbilisi", "Georgia", ["asia", "city"]),
    ("TPE", "Taipei", "Taiwan", ["asia", "city", "warm"]),
    ("VCP", "São Paulo Campinas", "Brazil", ["south_america", "latin_america", "city"]),
    ("ZNZ", "Zanzibar", "Tanzania", ["africa", "beach", "island", "warm"]),
]

ROUTES = [
    # ITA Airways via Rome.
    ("OSL", "FCO", "AZ", 190),
    ("FCO", "AGP", "AZ", 165),
    ("FCO", "ATH", "AZ", 120),
    ("FCO", "BCN", "AZ", 110),
    ("FCO", "BKK", "AZ", 615),
    ("FCO", "CAI", "AZ", 195),
    ("FCO", "DEL", "AZ", 455),
    ("FCO", "EZE", "AZ", 835),
    ("FCO", "GIG", "AZ", 705),
    ("FCO", "GRU", "AZ", 720),
    ("FCO", "HND", "AZ", 760),
    ("FCO", "JFK", "AZ", 580),
    ("FCO", "MLE", "AZ", 575),
    ("FCO", "MIA", "AZ", 650),
    # Condor via Frankfurt.
    ("FRA", "ANU", "DE", 550),
    ("FRA", "AUH", "DE", 380),
    ("FRA", "BGI", "DE", 560),
    ("FRA", "BKK", "DE", 660),
    ("FRA", "CPT", "DE", 720),
    ("FRA", "CUN", "DE", 700),
    ("FRA", "HKT", "DE", 675),
    ("FRA", "JFK", "DE", 520),
    ("FRA", "JNB", "DE", 650),
    ("FRA", "LAX", "DE", 700),
    ("FRA", "MBJ", "DE", 640),
    ("FRA", "MLE", "DE", 600),
    ("FRA", "MRU", "DE", 695),
    ("FRA", "PUJ", "DE", 620),
    ("FRA", "SEZ", "DE", 610),
    ("FRA", "SEA", "DE", 650),
    ("FRA", "SFO", "DE", 690),
    # flydubai secondary network via Dubai.
    ("DXB", "ALA", "FZ", 260),
    ("DXB", "BJV", "FZ", 270),
    ("DXB", "CMB", "FZ", 260),
    ("DXB", "DAC", "FZ", 290),
    ("DXB", "GYD", "FZ", 180),
    ("DXB", "HYD", "FZ", 215),
    ("DXB", "KBV", "FZ", 405),
    ("DXB", "KHI", "FZ", 125),
    ("DXB", "KTM", "FZ", 250),
    ("DXB", "LGK", "FZ", 430),
    ("DXB", "MBA", "FZ", 330),
    ("DXB", "MLE", "FZ", 250),
    ("DXB", "PEN", "FZ", 425),
    ("DXB", "TAS", "FZ", 220),
    ("DXB", "TBS", "FZ", 210),
    ("DXB", "ZNZ", "FZ", 345),
    # SriLankan via Colombo.
    ("DXB", "CMB", "UL", 260),
    ("DOH", "CMB", "UL", 295),
    ("LHR", "CMB", "UL", 650),
    ("CDG", "CMB", "UL", 620),
    ("FRA", "CMB", "UL", 600),
    ("CMB", "BKK", "UL", 220),
    ("CMB", "DEL", "UL", 215),
    ("CMB", "KUL", "UL", 215),
    ("CMB", "MLE", "UL", 90),
    ("CMB", "MEL", "UL", 610),
    ("CMB", "NRT", "UL", 520),
    ("CMB", "SIN", "UL", 235),
    ("CMB", "SYD", "UL", 640),
    # EVA via Taipei, fed from London/Paris/Munich/Amsterdam/Vienna.
    ("LHR", "TPE", "BR", 800),
    ("CDG", "TPE", "BR", 780),
    ("MUC", "TPE", "BR", 760),
    ("AMS", "TPE", "BR", 770),
    ("VIE", "TPE", "BR", 750),
    ("TPE", "BKK", "BR", 230),
    ("TPE", "DPS", "BR", 330),
    ("TPE", "HAN", "BR", 190),
    ("TPE", "HKG", "BR", 110),
    ("TPE", "KIX", "BR", 160),
    ("TPE", "MNL", "BR", 140),
    ("TPE", "NRT", "BR", 190),
    ("TPE", "PNH", "BR", 215),
    ("TPE", "PVG", "BR", 110),
    ("TPE", "SGN", "BR", 210),
    ("TPE", "SIN", "BR", 270),
    # India / South Asia with IndiGo.
    ("DXB", "DEL", "6E", 205),
    ("DXB", "BOM", "6E", 180),
    ("DXB", "BLR", "6E", 235),
    ("DXB", "COK", "6E", 245),
    ("DXB", "HYD", "6E", 215),
    ("DOH", "DEL", "6E", 220),
    ("DEL", "BKK", "6E", 245),
    ("DEL", "BLR", "6E", 165),
    ("DEL", "CCU", "6E", 135),
    ("DEL", "COK", "6E", 190),
    ("DEL", "HKT", "6E", 265),
    ("DEL", "KTM", "6E", 105),
    ("DEL", "MLE", "6E", 270),
    # Qantas, Jetstar and Virgin Australia inside Oceania and to Asia.
    ("SIN", "MEL", "QF", 460),
    ("SIN", "SYD", "QF", 465),
    ("PER", "LHR", "QF", 1020),
    ("SYD", "AKL", "QF", 190),
    ("SYD", "BNE", "QF", 90),
    ("SYD", "CHC", "QF", 185),
    ("SYD", "MEL", "QF", 95),
    ("SYD", "NAN", "QF", 240),
    ("SYD", "PER", "QF", 300),
    ("SYD", "SIN", "QF", 495),
    ("SYD", "OOL", "JQ", 80),
    ("MEL", "DPS", "JQ", 370),
    ("MEL", "HKT", "JQ", 530),
    ("MEL", "SIN", "JQ", 470),
    ("MEL", "SYD", "JQ", 95),
    ("BNE", "DPS", "JQ", 390),
    ("BNE", "NAN", "JQ", 220),
    ("BNE", "SYD", "JQ", 90),
    ("SYD", "BNE", "VA", 90),
    ("SYD", "MEL", "VA", 95),
    ("SYD", "OOL", "VA", 80),
    ("BNE", "DPS", "VA", 390),
    ("BNE", "NAN", "VA", 220),
    ("MEL", "DPS", "VA", 370),
    # Western Europe leisure carriers.
    ("BCN", "AGP", "VY", 100),
    ("BCN", "ALC", "VY", 75),
    ("BCN", "ATH", "VY", 170),
    ("BCN", "FCO", "VY", 110),
    ("BCN", "LPA", "VY", 205),
    ("BCN", "NCE", "VY", 80),
    ("BCN", "PMI", "VY", 55),
    ("BCN", "TFS", "VY", 215),
    ("ORY", "AGP", "TO", 155),
    ("ORY", "ALC", "TO", 130),
    ("ORY", "ATH", "TO", 195),
    ("ORY", "FCO", "TO", 120),
    ("ORY", "LIS", "TO", 150),
    ("ORY", "MRS", "TO", 80),
    ("ORY", "NCE", "TO", 85),
    ("ORY", "RAK", "TO", 190),
    ("CDG", "ORY", "AF", 45),
    # Air Transat Canada leisure.
    ("CDG", "YUL", "TS", 455),
    ("CDG", "YYZ", "TS", 485),
    ("AMS", "YYZ", "TS", 480),
    ("LIS", "YUL", "TS", 420),
    ("YUL", "CUN", "TS", 285),
    ("YUL", "PUJ", "TS", 275),
    ("YUL", "SDQ", "TS", 285),
    ("YYZ", "CUN", "TS", 250),
    ("YYZ", "PUJ", "TS", 260),
    # Americas expansion.
    ("MAD", "MEX", "AM", 720),
    ("CDG", "MEX", "AM", 700),
    ("AMS", "MEX", "AM", 690),
    ("MEX", "CUN", "AM", 135),
    ("MEX", "GDL", "AM", 80),
    ("MEX", "LAX", "AM", 240),
    ("MEX", "LIM", "AM", 360),
    ("MEX", "SCL", "AM", 520),
    ("MAD", "BOG", "AV", 635),
    ("LHR", "BOG", "AV", 660),
    ("BOG", "CTG", "AV", 90),
    ("BOG", "LIM", "AV", 190),
    ("BOG", "MDE", "AV", 60),
    ("BOG", "MIA", "AV", 225),
    ("BOG", "SCL", "AV", 360),
    ("BOG", "UIO", "AV", 95),
    ("MAD", "EZE", "AR", 780),
    ("FCO", "EZE", "AR", 835),
    ("MIA", "EZE", "AR", 540),
    ("EZE", "COR", "AR", 85),
    ("EZE", "GIG", "AR", 180),
    ("EZE", "MVD", "AR", 50),
    ("EZE", "SCL", "AR", 125),
    ("FLL", "CNF", "AD", 480),
    ("FLL", "REC", "AD", 430),
    ("FLL", "VCP", "AD", 510),
    ("LIS", "VCP", "AD", 590),
    ("VCP", "BSB", "AD", 100),
    ("VCP", "CNF", "AD", 75),
    ("VCP", "CWB", "AD", 70),
    ("VCP", "FOR", "AD", 210),
    ("VCP", "GIG", "AD", 70),
    ("VCP", "REC", "AD", 185),
    ("VCP", "SSA", "AD", 145),
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
