#!/usr/bin/env python3
"""Free-first travel tips prototype for ID travel route discovery."""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Any


DATA_DIR = Path(__file__).resolve().parent / "data"
DEFAULT_LAYOVER_MIN = 90


@dataclass(frozen=True)
class Leg:
    origin: str
    destination: str
    airline: str
    duration_min: int
    confidence: str


@dataclass(frozen=True)
class Itinerary:
    legs: tuple[Leg, ...]
    destination: str
    duration_min: int

    @property
    def stops(self) -> int:
        return max(0, len(self.legs) - 1)

    @property
    def airlines(self) -> tuple[str, ...]:
        return tuple(leg.airline for leg in self.legs)

    @property
    def route(self) -> str:
        points = [self.legs[0].origin]
        points.extend(leg.destination for leg in self.legs)
        return "-".join(points)


def load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def load_eligible_airlines() -> dict[str, str]:
    data = load_json(DATA_DIR / "eligible_airlines.json")
    return {item["code"].upper(): item["name"] for item in data["airlines"]}


def load_destinations(region: str, exact_destination: str = "") -> dict[str, dict[str, Any]]:
    data = load_json(DATA_DIR / "destinations.json")
    if exact_destination:
        for item in data["destinations"]:
            if item["iata"].upper() == exact_destination:
                return {exact_destination: item}
        return {
            exact_destination: {
                "iata": exact_destination,
                "city": exact_destination,
                "country": "Custom destination",
                "regions": ["all"],
            }
        }
    destinations = {}
    for item in data["destinations"]:
        if region == "all" or region in item.get("regions", []):
            destinations[item["iata"].upper()] = item
    return destinations


def load_legs(eligible: dict[str, str]) -> list[Leg]:
    data = load_json(DATA_DIR / "routes_sample.json")
    legs: list[Leg] = []
    for item in data["legs"]:
        airline = item["airline"].upper()
        if airline not in eligible:
            continue
        leg = Leg(
            origin=item["origin"].upper(),
            destination=item["destination"].upper(),
            airline=airline,
            duration_min=int(item["duration_min"]),
            confidence=item.get("confidence", "starter"),
        )
        legs.append(leg)
        legs.append(
            Leg(
                origin=leg.destination,
                destination=leg.origin,
                airline=leg.airline,
                duration_min=leg.duration_min,
                confidence=leg.confidence,
            )
        )
    return legs


def load_availability() -> dict[tuple[str, str, str], list[dict[str, Any]]]:
    path = DATA_DIR / "availability_overrides.json"
    if not path.exists():
        return {}
    data = load_json(path)
    checks: dict[tuple[str, str, str], list[dict[str, Any]]] = {}
    for item in data.get("checks", []):
        key = (item["origin"].upper(), item["destination"].upper(), item["airline"].upper())
        checks.setdefault(key, []).append(item)
    return checks


def build_adjacency(legs: list[Leg]) -> dict[str, list[Leg]]:
    adjacency: dict[str, list[Leg]] = {}
    for leg in legs:
        adjacency.setdefault(leg.origin, []).append(leg)
    return adjacency


def find_itineraries(
    origin: str,
    destinations: set[str],
    adjacency: dict[str, list[Leg]],
    max_stops: int,
    max_minutes: int,
) -> list[Itinerary]:
    max_legs = max_stops + 1
    found: list[Itinerary] = []

    def visit(current: str, legs: list[Leg], seen: set[str], elapsed: int) -> None:
        if legs and current in destinations:
            found.append(Itinerary(tuple(legs), current, elapsed))
        if len(legs) >= max_legs:
            return
        for leg in adjacency.get(current, []):
            if leg.destination in seen:
                continue
            extra = leg.duration_min if not legs else leg.duration_min + DEFAULT_LAYOVER_MIN
            if elapsed + extra > max_minutes:
                continue
            visit(leg.destination, [*legs, leg], {*seen, leg.destination}, elapsed + extra)

    visit(origin, [], {origin}, 0)
    return found


def has_return_route(itinerary: Itinerary, origin: str, adjacency: dict[str, list[Leg]], max_stops: int, max_minutes: int) -> bool:
    return bool(find_itineraries(itinerary.destination, {origin}, adjacency, max_stops, max_minutes))


def score_itinerary(itinerary: Itinerary, has_return: bool, availability_status: str) -> int:
    score = 1000
    score -= itinerary.duration_min
    score -= itinerary.stops * 120
    if len(set(itinerary.airlines)) == 1:
        score += 40
    if availability_status == "9plus":
        score += 200
    elif availability_status == "some":
        score += 60
    elif availability_status == "none":
        score -= 400
    if has_return:
        score += 150
    return score


def best_availability(
    itinerary: Itinerary,
    availability: dict[tuple[str, str, str], list[dict[str, Any]]],
    start: date,
    end: date,
) -> str:
    statuses = []
    for leg in itinerary.legs:
        checks = availability.get((leg.origin, leg.destination, leg.airline), [])
        for check in checks:
            check_date = check.get("date")
            if check_date:
                parsed_date = date.fromisoformat(check_date)
                if parsed_date < start or parsed_date > end:
                    continue
            statuses.append(check.get("status", "unknown"))
    if "none" in statuses:
        return "none"
    if "9plus" in statuses:
        return "9plus"
    if "some" in statuses:
        return "some"
    return "unknown"


def format_duration(minutes: int) -> str:
    hours, mins = divmod(minutes, 60)
    return f"{hours}h{mins:02d}"


def manual_check_hint(leg: Leg, start: date) -> str:
    return (
        "python3 manual_check.py add "
        f"--date {start.isoformat()} --origin {leg.origin} --destination {leg.destination} "
        f"--airline {leg.airline} --status 9plus"
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Find free-first ID travel tip candidates from sample route data")
    parser.add_argument("--from", dest="origin", default="OSL", help="Origin airport, e.g. OSL or BGO")
    parser.add_argument("--to", dest="destination", default="", help="Exact destination airport, e.g. ALC or MLE")
    parser.add_argument("--start", default="2026-11-01", help="Trip window start date")
    parser.add_argument("--end", default="2026-11-08", help="Trip window end date")
    parser.add_argument(
        "--region",
        default="warm_europe",
        help="Destination region, e.g. warm_europe, asia, japan, oceania, caribbean, north_america, beach, city, all",
    )
    parser.add_argument("--max-hours", type=float, default=30)
    parser.add_argument("--max-stops", type=int, default=2)
    parser.add_argument("--limit", type=int, default=20)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    start = date.fromisoformat(args.start)
    end = date.fromisoformat(args.end)
    if end < start:
        raise SystemExit("--end must be on or after --start")

    eligible = load_eligible_airlines()
    exact_destination = args.destination.strip().upper()
    if exact_destination and len(exact_destination) != 3:
        raise SystemExit("--to must be a 3-letter IATA airport code")
    destinations = load_destinations(args.region, exact_destination)
    legs = load_legs(eligible)
    availability = load_availability()
    adjacency = build_adjacency(legs)
    max_minutes = int(args.max_hours * 60)

    candidates = find_itineraries(args.origin.upper(), set(destinations), adjacency, args.max_stops, max_minutes)
    rows = []
    for itinerary in candidates:
        returnable = has_return_route(itinerary, args.origin.upper(), adjacency, args.max_stops, max_minutes)
        if not returnable:
            continue
        status = best_availability(itinerary, availability, start, end)
        rows.append((score_itinerary(itinerary, returnable, status), status, itinerary))

    rows.sort(key=lambda row: (-row[0], row[2].duration_min, row[2].stops, row[2].destination))

    target = f"to {exact_destination}" if exact_destination else f"region={args.region}"
    print(f"ID travel tips from {args.origin.upper()} | {start} to {end} | {target}")
    print(f"Data mode: free-first starter route map, not live schedules. Candidates: {len(rows)}\n")

    for index, (_, status, itinerary) in enumerate(rows[: args.limit], start=1):
        destination = destinations[itinerary.destination]
        airline_labels = " + ".join(f"{code} {eligible.get(code, '')}".strip() for code in itinerary.airlines)
        leg_labels = " / ".join(f"{leg.origin}-{leg.destination} {leg.airline}" for leg in itinerary.legs)
        print(f"{index:>2}. {destination['city']} ({itinerary.destination}), {destination['country']}")
        print(f"    Route: {itinerary.route} | {leg_labels}")
        print(f"    Airlines: {airline_labels}")
        print(f"    One-way estimate: {format_duration(itinerary.duration_min)} incl. assumed {DEFAULT_LAYOVER_MIN}m layover(s)")
        print(f"    Stops: {itinerary.stops} | 9-pax status: {status} | Return route: yes")
        print(f"    Next check: verify real dates/schedule, then search 9 adults")
        print("    Record result:")
        for leg in itinerary.legs:
            print(f"      {manual_check_hint(leg, start)}")
        print()

    if not rows:
        print("No round-trip candidates found with the current filters and starter route map.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
