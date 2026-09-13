#!/usr/bin/env python3
"""Refresh route freshness metadata from free/public source URLs.

This checks whether official/source pages still respond and optionally looks for
simple route markers in the page. It does not prove date-specific schedules.
"""

from __future__ import annotations

import argparse
import json
import socket
import sys
import urllib.error
import urllib.request
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any


ROUTES_PATH = Path("data/routes_sample.json")
APP_ROUTES_PATH = Path("outputs/id-travel-app/data/routes_sample.json")
USER_AGENT = "IDTravelRouteFreshness/0.1"
DESTINATIONS_PATH = Path("data/destinations.json")
AIRLINES_PATH = Path("data/eligible_airlines.json")
FETCH_CACHE: dict[str, tuple[int, str]] = {}


def load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def save_json(path: Path, payload: dict[str, Any]) -> None:
    with path.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2, ensure_ascii=False)
        handle.write("\n")


def route_marker_score(
    route: dict[str, Any],
    text: str,
    destinations: dict[str, dict[str, Any]],
    airlines: dict[str, str],
) -> tuple[str, list[str]]:
    text_lower = text.lower()
    origin = destinations.get(route["origin"], {})
    destination = destinations.get(route["destination"], {})
    airline_name = airlines.get(route["airline"], "")
    markers = [
        route["origin"].lower(),
        route["destination"].lower(),
        route["airline"].lower(),
        str(origin.get("city", "")).lower(),
        str(destination.get("city", "")).lower(),
        airline_name.lower(),
    ]
    matched = sorted({marker.upper() for marker in markers if marker and marker in text_lower})
    route_matched = (
        route["origin"].lower() in text_lower or str(origin.get("city", "")).lower() in text_lower
    ) and (
        route["destination"].lower() in text_lower or str(destination.get("city", "")).lower() in text_lower
    )
    if route_matched:
        return "source_and_route_markers_found", matched
    if len(matched) >= 2:
        return "source_responded_multiple_markers", matched
    if len(matched) == 1:
        return "source_responded_partial_markers", matched
    return "source_responded_no_markers", matched


def fetch_url(url: str) -> tuple[int, str]:
    if url in FETCH_CACHE:
        return FETCH_CACHE[url]
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=12) as response:
        status = int(getattr(response, "status", 200))
        content_type = response.headers.get("content-type", "")
        raw = response.read(750_000)
    if "text" not in content_type and "html" not in content_type and "json" not in content_type:
        FETCH_CACHE[url] = (status, "")
        return FETCH_CACHE[url]
    FETCH_CACHE[url] = (status, raw.decode("utf-8", errors="replace"))
    return FETCH_CACHE[url]


def refresh_route(
    route: dict[str, Any],
    today: str,
    destinations: dict[str, dict[str, Any]],
    airlines: dict[str, str],
) -> dict[str, Any]:
    source_url = route.get("source_url")
    if not source_url:
        return {
            "changed": False,
            "result": "skipped_no_source_url",
            "route": route,
        }

    try:
        status, text = fetch_url(source_url)
    except urllib.error.HTTPError as exc:
        route["last_checked_at"] = datetime.now(timezone.utc).isoformat()
        route["last_check_status"] = f"http_{exc.code}"
        route["last_check_ok"] = False
        return {"changed": True, "result": route["last_check_status"], "route": route}
    except urllib.error.URLError as exc:
        route["last_checked_at"] = datetime.now(timezone.utc).isoformat()
        route["last_check_status"] = f"url_error:{exc.reason}"
        route["last_check_ok"] = False
        return {"changed": True, "result": route["last_check_status"], "route": route}
    except (TimeoutError, socket.timeout):
        route["last_checked_at"] = datetime.now(timezone.utc).isoformat()
        route["last_check_status"] = "timeout"
        route["last_check_ok"] = False
        return {"changed": True, "result": "timeout", "route": route}

    route["last_checked_at"] = datetime.now(timezone.utc).isoformat()
    if 200 <= status < 400:
        result, markers = route_marker_score(route, text, destinations, airlines)
        route["last_check_status"] = result
        route["last_check_markers"] = markers
        route["last_check_ok"] = True
        if result in {"source_and_route_markers_found", "source_responded_multiple_markers"}:
            route["verified_at"] = today
            route["route_confidence"] = "high" if result == "source_and_route_markers_found" else "medium"
        if route.get("source_tier") not in {"A", "B"}:
            route["source_tier"] = "A"
        return {"changed": True, "result": result, "route": route}

    route["last_check_status"] = f"http_{status}"
    route["last_check_ok"] = False
    return {"changed": True, "result": route["last_check_status"], "route": route}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Refresh route freshness metadata from source URLs")
    parser.add_argument("--routes", default=str(ROUTES_PATH), help="Route JSON file to refresh")
    parser.add_argument("--write", action="store_true", help="Write updates back to the route file")
    parser.add_argument("--sync-app", action="store_true", help="Copy updated routes into the local web app data folder")
    parser.add_argument("--limit", type=int, help="Only check the first N routes with source_url")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    path = Path(args.routes)
    data = load_json(path)
    destinations_data = load_json(DESTINATIONS_PATH)
    airlines_data = load_json(AIRLINES_PATH)
    destinations = {item["iata"]: item for item in destinations_data.get("destinations", [])}
    airlines = {item["code"]: item["name"] for item in airlines_data.get("airlines", [])}
    today = date.today().isoformat()
    routes = data.get("legs", [])
    candidates = [route for route in routes if route.get("source_url")]
    if args.limit:
        candidates = candidates[: args.limit]

    if not candidates:
        print("No routes with source_url found.")
        return 0

    print(f"Checking {len(candidates)} route source URL(s)...")
    changed = 0
    for route in candidates:
        before = json.dumps(route, sort_keys=True)
        result = refresh_route(route, today, destinations, airlines)
        after = json.dumps(route, sort_keys=True)
        if before != after:
            changed += 1
        print(
            f"{route.get('origin')}-{route.get('destination')} {route.get('airline')}: "
            f"{result['result']}"
        )

    data["updated_at"] = today
    if args.write:
        save_json(path, data)
        print(f"Wrote {path} ({changed} route(s) changed).")
        if args.sync_app:
            save_json(APP_ROUTES_PATH, data)
            print(f"Synced {APP_ROUTES_PATH}.")
    else:
        print("Dry run only. Use --write to save changes.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
