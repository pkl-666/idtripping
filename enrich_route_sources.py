#!/usr/bin/env python3
"""Add best-known free/official source URLs to the prototype route map."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any


ROUTES_PATH = Path("data/routes_sample.json")
APP_ROUTES_PATH = Path("outputs/id-travel-app/data/routes_sample.json")
DESTINATIONS_PATH = Path("data/destinations.json")

CITY_SLUGS = {
    "AGP": "malaga",
    "ALC": "alicante",
    "AMS": "amsterdam",
    "ARN": "stockholm",
    "ATH": "athens",
    "AYT": "antalya",
    "BCN": "barcelona",
    "BGO": "bergen",
    "CDG": "paris",
    "CPH": "copenhagen",
    "DOH": "doha",
    "DXB": "dubai",
    "FAO": "faro",
    "FCO": "rome",
    "FRA": "frankfurt",
    "HEL": "helsinki",
    "HER": "heraklion",
    "IST": "istanbul",
    "LCA": "larnaca",
    "LHR": "london",
    "LIS": "lisbon",
    "LPA": "gran-canaria",
    "MAD": "madrid",
    "MLA": "malta",
    "MLE": "male",
    "MUC": "munich",
    "NCE": "nice",
    "OSL": "oslo",
    "PMI": "palma-de-mallorca",
    "TFS": "tenerife",
}

TITLE_SLUGS = {
    "AGP": "Malaga",
    "ALC": "Alicante",
    "AMS": "Amsterdam",
    "ARN": "Stockholm",
    "ATH": "Athens",
    "AYT": "Antalya",
    "BCN": "Barcelona",
    "BGO": "Bergen",
    "CDG": "Paris",
    "CPH": "Copenhagen",
    "DOH": "Doha",
    "DXB": "Dubai",
    "FAO": "Faro",
    "FCO": "Rome",
    "FRA": "Frankfurt",
    "HEL": "Helsinki",
    "HER": "Heraklion",
    "IST": "Istanbul",
    "LCA": "Larnaca",
    "LHR": "London",
    "LIS": "Lisbon",
    "LPA": "Gran-Canaria",
    "MAD": "Madrid",
    "MLA": "Malta",
    "MLE": "Male",
    "MUC": "Munich",
    "NCE": "Nice",
    "OSL": "Oslo",
    "PMI": "Palma-de-Mallorca",
    "TFS": "Tenerife",
}

BA_NETWORK = "https://www.britishairways.com/en-us/information/flight-information/our-route-network?link=main_nav"
WIDEROE_ROUTE_MAP = "https://www.wideroe.no/en/travel-information/route-map"
WIDEROE_DESTINATIONS = "https://www.wideroe.no/en/destinations"
AF_SUMMER_2026 = "https://corporate.airfrance.com/en/press-releases/air-frances-2026-summer-schedule"
AFKLM_NETWORK = "https://www.airfranceklm.com/en/group/strategy"


def load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def save_json(path: Path, payload: dict[str, Any]) -> None:
    with path.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2, ensure_ascii=False)
        handle.write("\n")


def kebab(value: str) -> str:
    cleaned = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return cleaned or value.lower()


def norwegian_url(route: dict[str, Any]) -> str:
    return f"https://www.norwegian.com/en/destinations/?D_City={route['destination']}"


def lufthansa_url(route: dict[str, Any]) -> str:
    origin = CITY_SLUGS.get(route["origin"], route["origin"].lower())
    destination = CITY_SLUGS.get(route["destination"], route["destination"].lower())
    return f"https://www.lufthansa.com/lhg/de/en/o-d/cy-cy/{origin}-{destination}"


def finnair_url(route: dict[str, Any]) -> str:
    origin_slug = TITLE_SLUGS.get(route["origin"], route["origin"])
    destination_slug = TITLE_SLUGS.get(route["destination"], route["destination"])
    return (
        "https://www.finnair.com/en/flights/city-to-city/"
        f"{route['origin'].lower()}/{route['destination'].lower()}/"
        f"flights-from-{origin_slug}-to-{destination_slug}"
    )


def transavia_url(route: dict[str, Any]) -> str:
    origin = CITY_SLUGS.get(route["origin"], route["origin"].lower())
    destination = CITY_SLUGS.get(route["destination"], route["destination"].lower())
    return f"https://www.transavia.com/airports/en-nl/amsterdam-airport-schiphol/{origin}-{destination}"


def iberia_url(route: dict[str, Any]) -> str:
    origin = TITLE_SLUGS.get(route["origin"], route["origin"]).replace("-", "")
    destination = TITLE_SLUGS.get(route["destination"], route["destination"]).replace("-", "")
    return f"https://www.iberia.com/us/cheap-flights/{origin}-{destination}/"


def tap_url(route: dict[str, Any]) -> str:
    origin = CITY_SLUGS.get(route["origin"], route["origin"].lower())
    destination = CITY_SLUGS.get(route["destination"], route["destination"].lower())
    return f"https://www.flytap.com/en_us/flights-from-{origin}-to-{destination}"


def qatar_url(route: dict[str, Any]) -> str:
    origin = CITY_SLUGS.get(route["origin"], route["origin"].lower())
    destination = CITY_SLUGS.get(route["destination"], route["destination"].lower())
    return f"https://www.qatarairways.com/en-gb/destinations/flights-to-{destination}/from-{origin}.html"


def emirates_url(route: dict[str, Any]) -> str:
    origin = CITY_SLUGS.get(route["origin"], route["origin"].lower())
    destination = CITY_SLUGS.get(route["destination"], route["destination"].lower())
    return f"https://www.emirates.com/english/destinations/{route['origin'].lower()}/{route['destination'].lower()}/flights-from-{origin}-to-{destination}/"


def set_source(route: dict[str, Any], url: str, source: str, confidence: str) -> bool:
    before = json.dumps(route, sort_keys=True)
    route["source_tier"] = "A"
    route["source"] = source
    route["source_url"] = url
    route["route_confidence"] = confidence
    route["confidence"] = "official_source_candidate" if confidence != "high" else "official_route_page"
    route.setdefault("verified_at", "")
    return before != json.dumps(route, sort_keys=True)


def enrich_route(route: dict[str, Any]) -> bool:
    airline = route["airline"]
    origin = route["origin"]
    destination = route["destination"]

    if airline in {"DY", "D8"}:
        return set_source(route, norwegian_url(route), "official Norwegian destination page", "medium")
    if airline == "WF":
        return set_source(route, WIDEROE_ROUTE_MAP, "official Widerøe route map", "medium")
    if airline == "LH":
        return set_source(route, lufthansa_url(route), "official Lufthansa route page", "high")
    if airline == "AY":
        return set_source(route, finnair_url(route), "official Finnair city-to-city page", "high")
    if airline == "BA":
        return set_source(route, BA_NETWORK, "official British Airways route network", "medium")
    if airline == "AF":
        url = AF_SUMMER_2026 if origin == "CDG" else AFKLM_NETWORK
        return set_source(route, url, "official Air France network information", "medium")
    if airline == "HV" and origin == "AMS":
        return set_source(route, transavia_url(route), "official Transavia route page", "high")
    if airline == "IB" and origin == "MAD":
        return set_source(route, iberia_url(route), "official Iberia route page", "high")
    if airline == "TP":
        return set_source(route, tap_url(route), "official TAP route page", "high")
    if airline == "EK":
        return set_source(route, emirates_url(route), "official Emirates route page", "high")
    if airline == "QR":
        return set_source(route, qatar_url(route), "official Qatar Airways route page", "high")

    if airline in {"A3", "PC", "XQ", "KM"}:
        route.setdefault("source_tier", "C")
        route.setdefault("source", "starter curated route map")
        route.setdefault("source_url", "")
        route.setdefault("verified_at", "")
        route.setdefault("route_confidence", "low")
        return False

    return False


def main() -> int:
    data = load_json(ROUTES_PATH)
    changed = 0
    sourced = 0
    for route in data.get("legs", []):
        if enrich_route(route):
            changed += 1
        if route.get("source_url"):
            sourced += 1

    save_json(ROUTES_PATH, data)
    save_json(APP_ROUTES_PATH, data)
    print(f"Updated {changed} route(s).")
    print(f"{sourced}/{len(data.get('legs', []))} route(s) now have a source_url.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
