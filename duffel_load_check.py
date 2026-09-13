#!/usr/bin/env python3
"""Small Duffel CLI proof-of-concept for commercial flight availability checks."""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from typing import Any


API_BASE = "https://api.duffel.com/air"
DEFAULT_QUANTITIES = [1, 2, 4, 6, 8, 9]
TARGET_AIRLINE_CODES = {"D8", "DY"}
TARGET_FLIGHT_NUMBER = "5021"
AVAILABILITY_HINTS = (
    "availability",
    "available",
    "capacity",
    "inventory",
    "quantity",
    "remaining",
    "seat",
)
FARE_HINTS = ("fare_basis", "fare_basis_code", "booking_class", "class")


class DuffelError(RuntimeError):
    pass


def request_json(method: str, path: str, token: str, body: dict[str, Any] | None = None) -> dict[str, Any]:
    data = json.dumps(body).encode("utf-8") if body is not None else None
    req = urllib.request.Request(
        f"{API_BASE}{path}",
        data=data,
        method=method,
        headers={
            "Authorization": f"Bearer {token}",
            "Duffel-Version": "v2",
            "Content-Type": "application/json",
            "Accept": "application/json",
        },
    )

    try:
        with urllib.request.urlopen(req, timeout=60) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        details = exc.read().decode("utf-8", errors="replace")
        raise DuffelError(f"Duffel HTTP {exc.code}: {details}") from exc
    except urllib.error.URLError as exc:
        raise DuffelError(f"Duffel request failed: {exc.reason}") from exc


def build_offer_request(origin: str, destination: str, departure_date: str, cabin_class: str, adults: int) -> dict[str, Any]:
    return {
        "data": {
            "slices": [
                {
                    "origin": origin,
                    "destination": destination,
                    "departure_date": departure_date,
                }
            ],
            "passengers": [{"type": "adult"} for _ in range(adults)],
            "cabin_class": cabin_class,
        }
    }


def create_offer_request(args: argparse.Namespace, token: str, adults: int) -> dict[str, Any]:
    body = build_offer_request(args.origin, args.destination, args.date, args.cabin, adults)
    query = urllib.parse.urlencode({"return_offers": "true"})
    return request_json("POST", f"/offer_requests?{query}", token, body)


def get_seat_maps(offer_id: str, token: str) -> dict[str, Any]:
    query = urllib.parse.urlencode({"offer_id": offer_id})
    return request_json("GET", f"/seat_maps?{query}", token)


def save_json(path: str, payload: dict[str, Any]) -> None:
    with open(path, "w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2, sort_keys=True)
        handle.write("\n")


def offers_from_response(payload: dict[str, Any]) -> list[dict[str, Any]]:
    data = payload.get("data", {})
    offers = data.get("offers", [])
    return offers if isinstance(offers, list) else []


def segments_for_offer(offer: dict[str, Any]) -> list[dict[str, Any]]:
    segments: list[dict[str, Any]] = []
    for slice_ in offer.get("slices", []) or []:
        segments.extend(slice_.get("segments", []) or [])
    return segments


def carrier_code(carrier: dict[str, Any] | None) -> str:
    if not isinstance(carrier, dict):
        return ""
    return carrier.get("iata_code") or carrier.get("iata") or carrier.get("id") or ""


def carrier_name(carrier: dict[str, Any] | None) -> str:
    if not isinstance(carrier, dict):
        return ""
    return carrier.get("name") or carrier.get("id") or ""


def place_code(place: dict[str, Any] | None) -> str:
    if not isinstance(place, dict):
        return ""
    return place.get("iata_code") or place.get("iata") or place.get("id") or ""


def aircraft_label(segment: dict[str, Any]) -> str:
    aircraft = segment.get("aircraft")
    if not isinstance(aircraft, dict):
        return ""
    name = aircraft.get("name") or aircraft.get("id") or ""
    code = aircraft.get("iata_code") or ""
    return f"{name} ({code})" if name and code else name or code


def segment_flight_number(segment: dict[str, Any]) -> str:
    return str(segment.get("marketing_carrier_flight_number") or segment.get("flight_number") or "")


def is_target_segment(segment: dict[str, Any]) -> bool:
    marketing = carrier_code(segment.get("marketing_carrier"))
    operating = carrier_code(segment.get("operating_carrier"))
    number = segment_flight_number(segment).lstrip("0")
    return (marketing in TARGET_AIRLINE_CODES or operating in TARGET_AIRLINE_CODES) and number == TARGET_FLIGHT_NUMBER


def collect_hint_fields(value: Any, hints: tuple[str, ...], prefix: str = "") -> list[tuple[str, Any]]:
    found: list[tuple[str, Any]] = []
    if isinstance(value, dict):
        for key, child in value.items():
            path = f"{prefix}.{key}" if prefix else key
            lower = key.lower()
            if any(hint in lower for hint in hints) and not isinstance(child, (dict, list)):
                found.append((path, child))
            found.extend(collect_hint_fields(child, hints, path))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            found.extend(collect_hint_fields(child, hints, f"{prefix}[{index}]"))
    return found


def compact_pairs(pairs: list[tuple[str, Any]], limit: int = 12) -> str:
    if not pairs:
        return "none exposed"
    rendered = [f"{path}={value}" for path, value in pairs[:limit]]
    if len(pairs) > limit:
        rendered.append(f"... +{len(pairs) - limit} more")
    return "; ".join(rendered)


def fare_fields(offer: dict[str, Any], segment: dict[str, Any]) -> str:
    pairs = collect_hint_fields(segment, FARE_HINTS)
    if not pairs:
        pairs = collect_hint_fields(offer, FARE_HINTS)
    return compact_pairs(pairs, limit=8)


def print_offer_summary(payload: dict[str, Any], adults: int) -> list[dict[str, Any]]:
    data = payload.get("data", {})
    offers = offers_from_response(payload)
    live_mode = data.get("live_mode")
    print(f"\n=== Duffel offer request: {adults} adult(s) ===")
    print(f"request_id: {data.get('id', 'unknown')} | live_mode: {live_mode} | offers: {len(offers)}")

    matching_offers: list[dict[str, Any]] = []
    for offer_index, offer in enumerate(offers, start=1):
        segments = segments_for_offer(offer)
        target = any(is_target_segment(segment) for segment in segments)
        if target:
            matching_offers.append(offer)

        marker = "MATCH D8/DY 5021" if target else "offer"
        print(
            f"\n[{offer_index}] {marker} | offer_id={offer.get('id')} | "
            f"price={offer.get('total_amount')} {offer.get('total_currency')}"
        )

        for segment in segments:
            marketing = segment.get("marketing_carrier") or {}
            operating = segment.get("operating_carrier") or {}
            origin = segment.get("origin") or {}
            destination = segment.get("destination") or {}
            print(
                "  "
                f"{carrier_code(marketing)}{segment_flight_number(segment)} "
                f"{place_code(origin)}->{place_code(destination)} "
                f"{segment.get('departing_at')} -> {segment.get('arriving_at')} | "
                f"marketing={carrier_name(marketing)} ({carrier_code(marketing)}) | "
                f"operating={carrier_name(operating)} ({carrier_code(operating)}) | "
                f"aircraft={aircraft_label(segment) or 'unknown'} | "
                f"segment_id={segment.get('id')}"
            )
            print(f"    fare/booking fields: {fare_fields(offer, segment)}")
            print(f"    availability-like fields: {compact_pairs(collect_hint_fields(segment, AVAILABILITY_HINTS))}")

        offer_availability = collect_hint_fields(offer, AVAILABILITY_HINTS)
        if offer_availability:
            print(f"  offer availability-like fields: {compact_pairs(offer_availability)}")

    if not matching_offers:
        print("\nNo offer matched Norwegian D8/DY flight number 5021.")
    return matching_offers


def seat_status_counts(seat_maps: dict[str, Any]) -> dict[str, int]:
    counts: dict[str, int] = {}

    def walk(value: Any) -> None:
        if isinstance(value, dict):
            if value.get("type") == "seat" or "designator" in value:
                status = str(value.get("available") if "available" in value else value.get("status", "unknown"))
                counts[status] = counts.get(status, 0) + 1
            for child in value.values():
                walk(child)
        elif isinstance(value, list):
            for child in value:
                walk(child)

    walk(seat_maps)
    return counts


def maybe_fetch_seat_maps(matching_offers: list[dict[str, Any]], token: str, limit: int) -> None:
    for offer in matching_offers[:limit]:
        offer_id = offer.get("id")
        if not offer_id:
            continue
        try:
            seat_maps = get_seat_maps(offer_id, token)
        except DuffelError as exc:
            print(f"\nSeat maps for {offer_id}: unavailable/error: {exc}")
            continue

        path = f"seat_maps_{offer_id}.json"
        save_json(path, seat_maps)
        counts = seat_status_counts(seat_maps)
        print(f"\nSeat-map indication for {offer_id}: saved {path}")
        print(f"  seat status counts: {counts or 'no seat elements found'}")
        print("  Note: this is a seat-map indication, not actual passenger load.")


def run_single(args: argparse.Namespace, token: str) -> list[dict[str, Any]]:
    payload = create_offer_request(args, token, args.adults)
    save_json(args.output, payload)
    print(f"Saved raw Duffel response to {args.output}")
    return print_offer_summary(payload, args.adults)


def run_quantity_sweep(args: argparse.Namespace, token: str) -> list[dict[str, Any]]:
    all_matches: list[dict[str, Any]] = []
    print("\n=== Quantity sweep ===")
    print("Do not infer actual load from these prices. This only tests commercial sellability.")
    for adults in DEFAULT_QUANTITIES:
        payload = create_offer_request(args, token, adults)
        output = f"duffel_response_{adults}.json"
        save_json(output, payload)
        matches = print_offer_summary(payload, adults)
        all_matches.extend(matches)
        cheapest = min(
            (offer for offer in matches if offer.get("total_amount") is not None),
            key=lambda offer: float(offer.get("total_amount")),
            default=None,
        )
        if cheapest:
            print(
                f"\nSweep result: {adults} adult(s): D85021 returned; "
                f"cheapest={cheapest.get('total_amount')} {cheapest.get('total_currency')}; "
                f"offer_id={cheapest.get('id')}"
            )
        else:
            print(f"\nSweep result: {adults} adult(s): D85021 not returned")
        time.sleep(args.pause)
    return all_matches


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Duffel non-rev commercial availability proof-of-concept")
    parser.add_argument("--origin", default="OSL")
    parser.add_argument("--destination", default="AGP")
    parser.add_argument("--date", default="2026-10-05")
    parser.add_argument("--cabin", default="economy")
    parser.add_argument("--adults", type=int, default=1)
    parser.add_argument("--output", default="duffel_response.json")
    parser.add_argument("--sweep", action="store_true", help="Test 1, 2, 4, 6, 8, and 9 adults")
    parser.add_argument("--seat-maps", action="store_true", help="Fetch seat maps for matching offers")
    parser.add_argument("--seat-map-limit", type=int, default=3)
    parser.add_argument("--pause", type=float, default=0.25, help="Pause between sweep requests")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    token = os.environ.get("DUFFEL_TOKEN")
    if not token:
        print("DUFFEL_TOKEN is not set. Export it in your shell before running this script.", file=sys.stderr)
        return 2

    print(f"Checked at {datetime.now(timezone.utc).isoformat()}")
    try:
        matches = run_quantity_sweep(args, token) if args.sweep else run_single(args, token)
        if args.seat_maps and matches:
            maybe_fetch_seat_maps(matches, token, args.seat_map_limit)
    except DuffelError as exc:
        print(str(exc), file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
