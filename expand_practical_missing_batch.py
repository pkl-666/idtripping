#!/usr/bin/env python3
"""Add more practical missing eligible airlines for route inspiration."""

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
    "3H": ("official Air Inuit flight schedule", "https://www.airinuit.com/en/book/flight/flight-schedule/regular-schedule-2026-08-03"),
    "4Y": ("official Discover Airlines timetable", "https://www.discover-airlines.com/us/en/homepage"),
    "5T": ("official Canadian North route map", "https://canadiannorth.com/plan_your_trip/route-map/"),
    "9M": ("Central Mountain Air route map reference", "https://www.flightconnections.com/route-map-central-mountain-air-9m"),
    "CD": ("official Corendon flight information", "https://www.corendon.nl/vluchtinformatie"),
    "CS": ("official Chair Airlines destinations page", "https://www.chair.ch/en/destinations-en"),
    "DI": ("official Marabu destinations page", "https://flymarabu.com/en/destinations"),
    "DM": ("official Arajet destinations page", "https://www.arajet.com/en-us/where-we-fly"),
    "EN": ("official Air Dolomiti routes page", "https://www.airdolomiti.eu/flights-europe"),
    "F8": ("official Flair Airlines destinations page", "https://flights.flyflair.com/en-us/destinations"),
    "GK": ("official Jetstar route map", "https://www.jetstar.com/jp/en/route-map"),
    "KC": ("official Air Astana route map", "https://www.airastana.com/chn-en/route-map"),
    "MX": ("official Breeze Airways city-to-city sitemap", "https://www.flybreeze.com/shopping/en-us/sitemap/city-to-city-flights/page-1"),
    "PK": ("official PIA route map", "https://www.piac.com.pk/where-we-fly/map?highlight=WyJvZiJd"),
    "VL": ("official Lufthansa destinations page", "https://www.lufthansa.com/lhg/xk/en"),
    "WN": ("official Southwest route map", "https://www.southwest.com/route-map/?clk=seo-vpstocrp-route-map"),
    "XC": ("official Corendon Airlines all-routes page", "https://www.corendonairlines.com/explore/all-routes"),
    "XR": ("official Corendon Airlines airports page", "https://www.corendonairlines.com/airports"),
}

DESTINATIONS = [
    ("AMS", "Amsterdam", "Netherlands", ["europe", "city"]),
    ("AAN", "Al Ain", "United Arab Emirates", ["middle_east", "city", "warm"]),
    ("ALA", "Almaty", "Kazakhstan", ["asia", "central_asia", "city"]),
    ("ARN", "Stockholm Arlanda", "Sweden", ["europe", "nordic", "city"]),
    ("AUA", "Aruba", "Aruba", ["caribbean", "beach", "island", "warm"]),
    ("BER", "Berlin", "Germany", ["europe", "city"]),
    ("BGO", "Bergen", "Norway", ["europe", "nordic", "city"]),
    ("BDL", "Hartford", "United States", ["north_america", "city"]),
    ("BGI", "Barbados", "Barbados", ["caribbean", "beach", "island", "warm"]),
    ("BLQ", "Bologna", "Italy", ["europe", "warm_europe", "city"]),
    ("BNA", "Nashville", "United States", ["north_america", "city"]),
    ("BOS", "Boston", "United States", ["north_america", "city"]),
    ("BRE", "Bremen", "Germany", ["europe", "city"]),
    ("BRI", "Bari", "Italy", ["europe", "warm_europe", "city", "beach"]),
    ("BSL", "Basel", "Switzerland", ["europe", "city"]),
    ("BWI", "Baltimore/Washington", "United States", ["north_america", "city"]),
    ("CDG", "Paris Charles de Gaulle", "France", ["europe", "city"]),
    ("CFU", "Corfu", "Greece", ["europe", "warm_europe", "beach", "island"]),
    ("CGN", "Cologne/Bonn", "Germany", ["europe", "city"]),
    ("CHS", "Charleston", "United States", ["north_america", "city", "warm"]),
    ("CHQ", "Chania", "Greece", ["europe", "warm_europe", "beach", "island"]),
    ("CIT", "Shymkent", "Kazakhstan", ["asia", "central_asia", "city"]),
    ("COR", "Córdoba", "Argentina", ["south_america", "latin_america", "city"]),
    ("CPH", "Copenhagen", "Denmark", ["europe", "nordic", "city"]),
    ("CTS", "Sapporo", "Japan", ["asia", "japan", "city"]),
    ("CTG", "Cartagena", "Colombia", ["south_america", "latin_america", "caribbean", "beach", "warm"]),
    ("CUR", "Curaçao", "Curaçao", ["caribbean", "beach", "island", "warm"]),
    ("DEN", "Denver", "United States", ["north_america", "city"]),
    ("DOH", "Doha", "Qatar", ["middle_east", "city", "warm"]),
    ("DXB", "Dubai", "United Arab Emirates", ["middle_east", "city", "warm"]),
    ("EVN", "Yerevan", "Armenia", ["asia", "city"]),
    ("FLR", "Florence", "Italy", ["europe", "warm_europe", "city"]),
    ("FNC", "Funchal", "Portugal", ["europe", "warm_europe", "beach", "island"]),
    ("FRA", "Frankfurt", "Germany", ["europe", "city"]),
    ("FUK", "Fukuoka", "Japan", ["asia", "japan", "city"]),
    ("GOA", "Genoa", "Italy", ["europe", "warm_europe", "city"]),
    ("GRZ", "Graz", "Austria", ["europe", "city"]),
    ("GRQ", "Groningen", "Netherlands", ["europe", "city"]),
    ("GYE", "Guayaquil", "Ecuador", ["south_america", "latin_america", "city", "warm"]),
    ("HAJ", "Hannover", "Germany", ["europe", "city"]),
    ("HEL", "Helsinki", "Finland", ["europe", "nordic", "city"]),
    ("HOU", "Houston Hobby", "United States", ["north_america", "city", "warm"]),
    ("HRG", "Hurghada", "Egypt", ["africa", "beach", "warm"]),
    ("ISB", "Islamabad", "Pakistan", ["asia", "city"]),
    ("JED", "Jeddah", "Saudi Arabia", ["middle_east", "city", "warm"]),
    ("KIN", "Kingston", "Jamaica", ["caribbean", "city", "warm"]),
    ("KGS", "Kos", "Greece", ["europe", "warm_europe", "beach", "island"]),
    ("KHI", "Karachi", "Pakistan", ["asia", "city", "warm"]),
    ("KIX", "Osaka Kansai", "Japan", ["asia", "japan", "city"]),
    ("KMI", "Miyazaki", "Japan", ["asia", "japan", "beach"]),
    ("KOA", "Kona", "United States", ["north_america", "oceania", "beach", "island", "warm"]),
    ("KOJ", "Kagoshima", "Japan", ["asia", "japan", "city"]),
    ("KRK", "Krakow", "Poland", ["europe", "city"]),
    ("KVA", "Kavala", "Greece", ["europe", "warm_europe", "beach"]),
    ("LEJ", "Leipzig/Halle", "Germany", ["europe", "city"]),
    ("LHE", "Lahore", "Pakistan", ["asia", "city"]),
    ("LHR", "London Heathrow", "United Kingdom", ["europe", "city"]),
    ("LIN", "Milan Linate", "Italy", ["europe", "warm_europe", "city"]),
    ("LNZ", "Linz", "Austria", ["europe", "city"]),
    ("LYS", "Lyon", "France", ["europe", "city"]),
    ("MBJ", "Montego Bay", "Jamaica", ["caribbean", "beach", "warm"]),
    ("MDE", "Medellín", "Colombia", ["south_america", "latin_america", "city", "warm"]),
    ("MDW", "Chicago Midway", "United States", ["north_america", "city"]),
    ("MFM", "Macau", "Macau", ["asia", "city"]),
    ("MUC", "Munich", "Germany", ["europe", "city"]),
    ("MSY", "New Orleans", "United States", ["north_america", "city", "warm"]),
    ("NGO", "Nagoya", "Japan", ["asia", "japan", "city"]),
    ("NQZ", "Astana", "Kazakhstan", ["asia", "central_asia", "city"]),
    ("NUE", "Nuremberg", "Germany", ["europe", "city"]),
    ("OKA", "Okinawa", "Japan", ["asia", "japan", "beach", "island"]),
    ("OLB", "Olbia", "Italy", ["europe", "warm_europe", "beach", "island"]),
    ("OSL", "Oslo", "Norway", ["europe", "nordic", "city"]),
    ("PHX", "Phoenix", "United States", ["north_america", "city", "warm"]),
    ("PRN", "Pristina", "Kosovo", ["europe", "city"]),
    ("PVD", "Providence", "United States", ["north_america", "city"]),
    ("PVK", "Preveza", "Greece", ["europe", "warm_europe", "beach"]),
    ("RAK", "Marrakesh", "Morocco", ["africa", "city", "warm"]),
    ("RDU", "Raleigh/Durham", "United States", ["north_america", "city"]),
    ("RHO", "Rhodes", "Greece", ["europe", "warm_europe", "beach", "island"]),
    ("RIC", "Richmond", "United States", ["north_america", "city"]),
    ("RMF", "Marsa Alam", "Egypt", ["africa", "beach", "warm"]),
    ("ROS", "Rosario", "Argentina", ["south_america", "latin_america", "city"]),
    ("RTM", "Rotterdam", "Netherlands", ["europe", "city"]),
    ("SCO", "Aktau", "Kazakhstan", ["asia", "central_asia", "city"]),
    ("SDQ", "Santo Domingo", "Dominican Republic", ["caribbean", "city", "warm"]),
    ("SKP", "Skopje", "North Macedonia", ["europe", "city"]),
    ("SSH", "Sharm el-Sheikh", "Egypt", ["africa", "beach", "warm"]),
    ("STR", "Stuttgart", "Germany", ["europe", "city"]),
    ("TAS", "Tashkent", "Uzbekistan", ["asia", "central_asia", "city"]),
    ("TRN", "Turin", "Italy", ["europe", "city"]),
    ("TRS", "Trieste", "Italy", ["europe", "city"]),
    ("VRN", "Verona", "Italy", ["europe", "warm_europe", "city"]),
    ("WDH", "Windhoek", "Namibia", ["africa", "city", "warm"]),
    ("XRY", "Jerez de la Frontera", "Spain", ["europe", "warm_europe", "city"]),
    ("YEG", "Edmonton", "Canada", ["north_america", "city"]),
    ("YEV", "Inuvik", "Canada", ["north_america", "arctic"]),
    ("YFB", "Iqaluit", "Canada", ["north_america", "arctic", "city"]),
    ("YGL", "La Grande", "Canada", ["north_america", "arctic"]),
    ("YLW", "Kelowna", "Canada", ["north_america", "city"]),
    ("YQB", "Québec City", "Canada", ["north_america", "city"]),
    ("YRT", "Rankin Inlet", "Canada", ["north_america", "arctic"]),
    ("YUL", "Montreal", "Canada", ["north_america", "city"]),
    ("YVP", "Kuujjuaq", "Canada", ["north_america", "arctic"]),
    ("YXS", "Prince George", "Canada", ["north_america", "city"]),
    ("YZF", "Yellowknife", "Canada", ["north_america", "arctic", "city"]),
]

ROUTES = [
    # Lufthansa Group, Germany/SWISS leisure.
    ("FRA", "CUN", "4Y", 690), ("FRA", "FUE", "4Y", 270), ("FRA", "HRG", "4Y", 285),
    ("FRA", "LPA", "4Y", 275), ("FRA", "MLE", "4Y", 600), ("FRA", "MCO", "4Y", 620),
    ("FRA", "MRU", "4Y", 690), ("FRA", "PMI", "4Y", 130), ("FRA", "PUJ", "4Y", 610),
    ("FRA", "TFS", "4Y", 280), ("FRA", "WDH", "4Y", 630), ("MUC", "PMI", "4Y", 130),
    ("FRA", "FLR", "EN", 85), ("FRA", "LUX", "EN", 45), ("FRA", "LYS", "EN", 80),
    ("FRA", "PRG", "EN", 65), ("FRA", "TRN", "EN", 75), ("FRA", "TRS", "EN", 80),
    ("MUC", "BLQ", "EN", 70), ("MUC", "BRI", "EN", 95), ("MUC", "FLR", "EN", 80),
    ("MUC", "GOA", "EN", 75), ("MUC", "GRZ", "EN", 55), ("MUC", "KRK", "EN", 75),
    ("MUC", "LIN", "EN", 65), ("MUC", "VCE", "EN", 65), ("MUC", "VRN", "EN", 60),
    ("MUC", "BER", "VL", 70), ("MUC", "BRE", "VL", 75), ("MUC", "DUS", "VL", 75),
    ("MUC", "HAM", "VL", 80), ("MUC", "HAJ", "VL", 70),
    # German/Dutch/Swiss leisure operators.
    ("HAM", "CHQ", "DI", 190), ("HAM", "CFU", "DI", 170), ("HAM", "FNC", "DI", 270),
    ("HAM", "FUE", "DI", 285), ("HAM", "HER", "DI", 195), ("HAM", "PMI", "DI", 165),
    ("LEJ", "FUE", "DI", 280), ("LEJ", "HRG", "DI", 270), ("LEJ", "PMI", "DI", 150),
    ("NUE", "KGS", "DI", 180), ("NUE", "LPA", "DI", 275), ("NUE", "OLB", "DI", 95),
    ("NUE", "RHO", "DI", 190), ("NUE", "TFS", "DI", 285),
    ("AMS", "CUR", "CD", 600), ("AMS", "HRG", "CD", 300), ("AMS", "PMI", "CD", 140),
    ("AMS", "OLB", "CD", 150), ("BRU", "HRG", "CD", 300), ("BRU", "PMI", "CD", 140),
    ("CGN", "AYT", "XC", 210), ("CGN", "HER", "XC", 195), ("DUS", "AYT", "XC", 215),
    ("DUS", "HER", "XC", 195), ("HAJ", "AYT", "XC", 210), ("NUE", "AYT", "XC", 190),
    ("NUE", "HER", "XC", 175), ("STR", "AYT", "XC", 190),
    ("BSL", "HRG", "XR", 265), ("BSL", "PMI", "XR", 115), ("DUS", "HRG", "XR", 290),
    ("FRA", "RMF", "XR", 285), ("HAM", "HRG", "XR", 300), ("ZRH", "TLV", "XR", 235),
    ("ZRH", "HRG", "CS", 260), ("ZRH", "KGS", "CS", 175), ("ZRH", "OPO", "CS", 155),
    ("ZRH", "PMI", "CS", 115), ("ZRH", "RAK", "CS", 220), ("ZRH", "RHO", "CS", 180),
    ("ZRH", "SKP", "CS", 125), ("ZRH", "PRN", "CS", 120), ("BSL", "PMI", "CS", 115),
    # Japan and Central Asia.
    ("NRT", "CTS", "GK", 105), ("NRT", "FUK", "GK", 125), ("NRT", "KIX", "GK", 90),
    ("NRT", "KMI", "GK", 115), ("NRT", "KOJ", "GK", 125), ("NRT", "OKA", "GK", 190),
    ("KIX", "CTS", "GK", 115), ("KIX", "OKA", "GK", 130), ("NGO", "FUK", "GK", 80),
    ("FRA", "ALA", "KC", 440), ("LHR", "ALA", "KC", 420), ("IST", "ALA", "KC", 310),
    ("DXB", "ALA", "KC", 260), ("ALA", "NQZ", "KC", 105), ("ALA", "CIT", "KC", 75),
    ("ALA", "SCO", "KC", 180), ("ALA", "TAS", "KC", 95), ("ALA", "DEL", "KC", 210),
    ("ALA", "BKK", "KC", 395), ("ALA", "ICN", "KC", 365),
    ("LHR", "ISB", "PK", 465), ("LHR", "KHI", "PK", 470), ("LHR", "LHE", "PK", 465),
    ("DXB", "ISB", "PK", 190), ("DXB", "KHI", "PK", 125), ("DXB", "LHE", "PK", 190),
    ("JED", "ISB", "PK", 285), ("JED", "KHI", "PK", 240), ("KHI", "ISB", "PK", 120),
    ("KHI", "LHE", "PK", 105),
    # Caribbean / Americas low-cost networks.
    ("SDQ", "AUA", "DM", 80), ("SDQ", "BOG", "DM", 150), ("SDQ", "CTG", "DM", 125),
    ("SDQ", "CUR", "DM", 85), ("SDQ", "EWR", "DM", 250), ("SDQ", "GRU", "DM", 420),
    ("SDQ", "GUA", "DM", 190), ("SDQ", "KIN", "DM", 90), ("SDQ", "MDE", "DM", 140),
    ("SDQ", "MEX", "DM", 260), ("SDQ", "MIA", "DM", 135), ("SDQ", "SJO", "DM", 175),
    ("SDQ", "SXM", "DM", 75), ("PUJ", "EZE", "DM", 480), ("PUJ", "GRU", "DM", 420),
    ("PUJ", "YUL", "DM", 275), ("PUJ", "YYZ", "DM", 270),
    ("YYZ", "CUN", "F8", 245), ("YYZ", "FLL", "F8", 190), ("YYZ", "MCO", "F8", 175),
    ("YYZ", "PUJ", "F8", 260), ("YYZ", "YVR", "F8", 310), ("YYZ", "YYC", "F8", 250),
    ("YUL", "FLL", "F8", 210), ("YVR", "CUN", "F8", 360), ("YVR", "GDL", "F8", 300),
    ("YVR", "PVR", "F8", 295),
    ("BOS", "CHS", "MX", 140), ("BOS", "MSY", "MX", 205), ("MCO", "BDL", "MX", 155),
    ("MCO", "CHS", "MX", 75), ("MCO", "MSY", "MX", 105), ("MCO", "PVD", "MX", 160),
    ("MCO", "RDU", "MX", 90), ("RDU", "CUN", "MX", 190), ("RIC", "MCO", "MX", 115),
    ("BWI", "MCO", "WN", 140), ("BWI", "FLL", "WN", 155), ("BWI", "CUN", "WN", 215),
    ("MDW", "DEN", "WN", 155), ("MDW", "LAS", "WN", 240), ("MDW", "MCO", "WN", 160),
    ("DEN", "LAS", "WN", 115), ("DEN", "PHX", "WN", 110), ("HOU", "CUN", "WN", 135),
    ("HOU", "LAS", "WN", 190), ("HOU", "MCO", "WN", 135), ("OAK", "HNL", "WN", 335),
    ("OAK", "KOA", "WN", 340),
    # Canada north and regional.
    ("YOW", "YFB", "5T", 190), ("YEG", "YZF", "5T", 105), ("YZF", "YEV", "5T", 120),
    ("YZF", "YRT", "5T", 110), ("YFB", "YRT", "5T", 115), ("YUL", "YVP", "5T", 140),
    ("YVP", "YFB", "5T", 90), ("YUL", "YVP", "3H", 140), ("YUL", "YGL", "3H", 95),
    ("YVP", "YGL", "3H", 95), ("YQB", "YUL", "3H", 50), ("YVR", "YXS", "9M", 85),
    ("YVR", "YLW", "9M", 60), ("YEG", "YXS", "9M", 95), ("YYC", "YXS", "9M", 95),
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
