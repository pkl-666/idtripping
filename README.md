# Duffel Non-Rev Load Checker POC

Tiny private CLI proof-of-concept for checking whether a commercial itinerary is still sellable through Duffel.

## Security

Do not put the Duffel token in source code or commit it. The script reads:

```sh
export DUFFEL_TOKEN="..."
```

`.env`, raw Duffel responses, seat-map responses, and local Python cache files are ignored by `.gitignore`.

## First Test

```sh
python3 duffel_load_check.py
```

Defaults:

- airline search context: OSL to AGP
- date: 2026-10-05
- cabin: economy
- passengers: 1 adult

The raw response is saved to `duffel_response.json`.

## Quantity Sweep

```sh
python3 duffel_load_check.py --sweep
```

This checks 1, 2, 4, 6, 8, and 9 adults. If D8/DY flight number 5021 is still returned at 9 adults, that supports a lower-bound statement like "9+ commercially sellable seats". It does not reveal actual load.

## Seat Maps

```sh
python3 duffel_load_check.py --seat-maps
python3 duffel_load_check.py --sweep --seat-maps
```

If Duffel returns D85021 offers and seat maps are supported for that offer, the script saves `seat_maps_<offer_id>.json` and prints counts by the statuses exposed in the seat-map response. Treat this only as "seat-map indication", not actual passenger load.

## Current Duffel Notes

- Duffel `POST /air/offer_requests?return_offers=true` returns offers for an offer request.
- Duffel Seat Maps are requested with `GET /air/seat_maps?offer_id=...`.
- Seat maps are not available for all airlines or flights.
- A Duffel test token may not return real Norwegian schedules or inventory. If test mode does not return D85021, stop before UI work and move to Duffel live-mode/account activation checks.

## Travel Tips Prototype

The free-first travel tips prototype uses:

- `data/eligible_airlines.json` from the myIDTravel screenshots
- `data/destinations.json` for region tags
- `data/routes_sample.json` as a starter route map, not live schedules
- `data/availability_overrides.json` for manual 9-pax statuses

Run an OSL warm-Europe search:

```sh
python3 travel_tips.py --from OSL --start 2026-11-04 --end 2026-11-12 --region warm_europe --max-hours 30 --max-stops 2
```

Run a BGO search:

```sh
python3 travel_tips.py --from BGO --start 2026-11-04 --end 2026-11-12 --region warm_europe --max-hours 30 --max-stops 2
```

Beach-focused, shorter trip candidates:

```sh
python3 travel_tips.py --from OSL --start 2026-11-04 --end 2026-11-12 --region beach --max-hours 8 --max-stops 1
```

The output is deliberately conservative: `9-pax status` is `unknown` unless there is a manual or API check for the requested date window.

## Manual 9-Pax Checks

Use `manual_check.py` to record free/manual availability indicators after checking 9 adults on an airline booking site.

List saved checks:

```sh
python3 manual_check.py list
```

Add or update a check:

```sh
python3 manual_check.py add --date 2026-11-04 --origin OSL --destination AGP --airline DY --status 9plus
```

Statuses:

- `9plus`: 9 adults could be priced/selected, so the indicator is 9+ commercially sellable seats
- `some`: the flight appears sellable, but not for 9 adults
- `none`: the flight was not sellable or not shown
- `unknown`: checked but inconclusive

Optional flight number and notes:

```sh
python3 manual_check.py add --date 2026-11-04 --origin OSL --destination AGP --airline D8 --flight-number 5021 --status 9plus --notes "manual Norwegian website check"
```

`travel_tips.py` prints a ready-to-run `manual_check.py add ...` command for each candidate. Change `--status` before running it if the result is not `9plus`.

## Local Web App

The browser prototype lives in `outputs/id-travel-app`.

If the local server is running, open:

```text
http://127.0.0.1:8766/
```

The app can:

- filter trip candidates by origin, date window, region, travel time, and stops
- choose common Norwegian bases as origins: OSL, BGO, ARN, CPH, AGP, ALC, RIX, PMI, and LPA
- override the origin with any 3-letter IATA code
- search a specific origin-to-destination airport pair with the `To IATA` field
- search by destination idea, such as `Maldives`, `Malé`, or `MLE`
- switch between card view and a map view of reachable destinations
- tap a map destination or cluster to open a compact route summary
- use month presets, such as February 2027
- emphasize route quality and backup alternatives over load estimates
- show an ID outlook of `Green`, `Yellow`, `Red`, or `Unknown`
- record manual 9-pax checks per leg in browser local storage
- warn when a saved check is older than 7 days
- export and import manual checks as JSON
- add custom route legs in the browser and export them as JSON

The web app still uses starter route data, not live schedules. Custom route legs are saved in the browser's local storage until exported or cleared.

The starter route map has been expanded with more eligible carriers and hubs. Current route-data carriers include Norwegian/Norwegian Air Sweden, Widerøe, Icelandair, Lufthansa, SWISS, Austrian, Brussels Airlines, LOT, Eurowings, British Airways, Air France, Finnair, TAP, Iberia, Transavia, Emirates, Qatar, Etihad, Air Canada, United, Delta, American Airlines, Air India, and selected warm-Europe carriers.

Example destination idea:

```text
From: OSL
Destination idea: Maldives
Month: February 2027
Region: Indian Ocean
Max stops: Up to 2 stops
Max one-way travel time: 30 hours
```

This currently returns Maldives/Malé candidates via Emirates/Dubai and Qatar/Doha, including backup routes via Copenhagen or Stockholm where present in the starter route map.

Specific route example:

```text
From: Riga (RIX)
To IATA: ALC
Max stops: Up to 2 stops
Max one-way travel time: 12 hours
```

When `To IATA` is filled, it overrides the region and destination idea filters and works as a route finder.

Map view:

```text
From: OSL
Start: 2027-01-10
End: 2027-01-22
Region: Asia
Max stops: Up to 2 stops
Map
```

The map view uses the same filters as the card list. It uses Leaflet, OpenStreetMap tiles, marker clustering, and `data/airports.json` coordinates. A destination tap opens a bottom sheet with the best route idea, estimated one-way travel time, stops, and rough time at destination. The time-at-destination number is currently a simple estimate based on the date window minus estimated round-trip travel time, not real schedules. The map requires internet access for the Leaflet CDN and map tiles.

Other useful examples:

```text
Region: North America
Max stops: Up to 2 stops
Max one-way travel time: 24 hours
```

```text
Region: Nordic
From: Bergen
Max stops: Up to 1 stop
```

Global idea examples:

```text
Region: Oceania
Destination idea: Sydney
Max stops: Up to 2 stops
Max one-way travel time: 36 hours
```

```text
Region: Japan
Max stops: Up to 2 stops
Max one-way travel time: 28 hours
```

```text
Region: Caribbean
Max stops: Up to 2 stops
Max one-way travel time: 28 hours
```

These regions rely heavily on hub routing through DXB, DOH, AUH, MCT, HEL, LHR, MIA, YYZ, and JFK. They are route ideas, not proof that a specific date operates.

```text
Region: South America
Max stops: Up to 2 stops
Max one-way travel time: 32 hours
```

South America currently uses routing through MAD, LIS, CDG, LHR, MIA, and JFK, with Iberia, Air Europa, TAP, Air France, British Airways, LATAM, and American Airlines as the main source carriers.

Check eligible airline route coverage:

```sh
python3 route_coverage.py
```

Coverage expansion scripts can be rerun safely; they only add missing route/destination entries:

```sh
python3 expand_airline_network.py
python3 expand_global_regions.py
python3 expand_south_america.py
python3 expand_high_value_missing.py
python3 expand_next_missing_batch.py
python3 expand_regional_island_batch.py
python3 expand_practical_missing_batch.py
python3 expand_norwegian_bases.py
```

The latest high-value batch adds more coverage for ITA Airways, Condor, flydubai, SriLankan, EVA Air, IndiGo, Qantas, Jetstar, Virgin Australia, Vueling, Transavia France, Air Transat, Aeromexico, Avianca, Aerolineas Argentinas, and Azul.

The next missing-airline batch adds Alaska Airlines, WestJet, Porter, French bee, Air Caraïbes, STARLUX, Fiji Airways, Binter Canarias, Canaryfly, Volotea, TUIfly, Viva Aerobus, and more Qantas/Jetstar/Virgin Australia coverage.

The regional/island batch adds Air Greenland, Atlantic Airways, Loganair, Luxair, Croatia Airlines, Smartwings, Azores Airlines/SATA, Cabo Verde Airlines, Binter Cabo Verde, Air Niugini, Aircalin, Air Calédonie, Air Austral, Air Rarotonga, Edelweiss, and EL AL. It also adds Africa, Azores, and Greenland as useful region filters in the web app.

The practical missing-airline batch adds Discover Airlines, Air Dolomiti, Lufthansa City Airlines, Marabu, Corendon/Chair leisure routes, Jetstar Japan, Air Astana, Pakistan International, Arajet, Flair, Breeze, Southwest, Canadian North, Air Inuit, and Central Mountain Air. It also adds Central Asia and Arctic as web-app region filters.

The Norwegian bases batch adds Riga as a destination/origin and starter Norwegian Air Sweden routes from Riga, including Riga-Alicante, Riga-Oslo, Riga-Stockholm, Riga-Copenhagen, Riga-Corfu, Riga-Tivat, and Bergen-Riga.

## Availability Adapters

`data/availability_adapters.json` defines the free-first live-check strategy per airline.

Current approach:

- `manual_link`: open the airline's official booking flow and manually search up to 9 adults
- `manual_search`: fallback when no airline-specific URL/instructions have been added yet

The app uses this file to show an `Open check` button per leg where a booking URL exists. It does not scrape airline websites or automate myIDTravel.

## Route Freshness

Route legs now support metadata for the best free verification we have:

- `source_tier`: `A` official airline/airport source, `B` public route dataset, `C` manually curated starter route, `D` uncertain/prototype data
- `source_url`: where the route was checked
- `verified_at`: date the source was checked
- `route_confidence`: high, medium, or low

The app displays `Fresh`, `Aging`, `Stale`, or `Unverified` per leg. `Fresh` means the route source was checked recently; it does not guarantee the route operates on a specific date.

Use `Review routes` in the web app to see routes that need verification.

Refresh routes with source URLs:

```sh
python3 refresh_routes.py --write --sync-app
```

Successful checks update `verified_at`. Failed checks, for example a timeout, are stored as `last_check_status` but do not prove the route has stopped operating.

Current caveat: many airline websites return `http_403` to simple script checks even when the page is valid in a normal browser. Treat those as "source link exists, automated freshness blocked", not as a dead route. A later Playwright/browser refresh can improve this for airlines such as Norwegian, Lufthansa, Finnair, Air France, Transavia, and Iberia.
