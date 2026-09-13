const DATA_PATHS = {
  airlines: "./data/eligible_airlines.json",
  destinations: "./data/destinations.json",
  routes: "./data/routes_sample.json",
  availability: "./data/availability_overrides.json",
  adapters: "./data/availability_adapters.json",
  airports: "./data/airports.json",
};

const LAYOVER_MIN = 90;
const STORAGE_KEY = "idTravelManualChecks";
const ROUTES_STORAGE_KEY = "idTravelCustomRoutes";
const STALE_DAYS = 7;
const STATUS_LABELS = {
  "9plus": "9+",
  some: "Some",
  none: "None",
  unknown: "Unknown",
};
const STATUS_CLASSES = {
  "9plus": "good",
  some: "some",
  none: "none",
  unknown: "unknown",
};
const AIRPORT_COORDS = {
  AAL: [57.09, 9.85], ABZ: [57.20, -2.20], ACE: [28.95, -13.61], AGP: [36.67, -4.49],
  ALC: [38.28, -0.56], ALA: [43.35, 77.04], AMS: [52.31, 4.76], ARN: [59.65, 17.92],
  ATH: [37.94, 23.94], AUA: [12.50, -70.02], AUH: [24.43, 54.65], AYT: [36.90, 30.79],
  BCN: [41.30, 2.08], BER: [52.37, 13.50], BGO: [60.29, 5.22], BKK: [13.69, 100.75],
  BNE: [-27.38, 153.12], BOS: [42.36, -71.01], BRU: [50.90, 4.48], BSL: [47.59, 7.53],
  BVC: [16.14, -22.89], BWI: [39.18, -76.67], CAI: [30.12, 31.41], CDG: [49.01, 2.55],
  CPH: [55.62, 12.65], CPT: [-33.97, 18.60], CTG: [10.44, -75.51], CUN: [21.04, -86.87],
  CUR: [12.19, -68.96], DEL: [28.56, 77.10], DEN: [39.86, -104.67], DOH: [25.27, 51.61],
  DPS: [-8.75, 115.17], DUB: [53.43, -6.25], DUS: [51.29, 6.77], DXB: [25.25, 55.36],
  EDI: [55.95, -3.36], EWR: [40.69, -74.17], EZE: [-34.82, -58.54], FAE: [62.06, -7.28],
  FAO: [37.01, -7.97], FCO: [41.80, 12.24], FLL: [26.07, -80.15], FRA: [50.04, 8.56],
  FUE: [28.45, -13.86], GDL: [20.52, -103.31], GIG: [-22.81, -43.25], GOH: [64.19, -51.68],
  GRU: [-23.43, -46.47], HKG: [22.31, 113.92], HND: [35.55, 139.78], HNL: [21.32, -157.92],
  HRG: [27.18, 33.80], IST: [41.26, 28.74], JAV: [69.24, -51.06], JFK: [40.64, -73.78],
  JNB: [-26.13, 28.24], KEF: [63.99, -22.62], KIX: [34.43, 135.23], KUL: [2.75, 101.71],
  LAX: [33.94, -118.41], LCA: [34.88, 33.62], LGW: [51.15, -0.19], LHR: [51.47, -0.45],
  LIS: [38.77, -9.13], LPA: [27.93, -15.39], MAD: [40.49, -3.57], MCO: [28.43, -81.31],
  MEX: [19.44, -99.07], MIA: [25.79, -80.29], MLE: [4.19, 73.53], MNL: [14.51, 121.02],
  MRU: [-20.43, 57.68], MUC: [48.35, 11.79], NAN: [-17.75, 177.44], NCE: [43.66, 7.22],
  NRT: [35.77, 140.39], OPO: [41.24, -8.68], ORY: [48.72, 2.38], OSL: [60.19, 11.10],
  PER: [-31.94, 115.97], PMI: [39.55, 2.74], POM: [-9.44, 147.22], PPT: [-17.56, -149.61],
  PRG: [50.10, 14.26], PUJ: [18.57, -68.36], RAI: [14.92, -23.49], RAR: [-21.20, -159.81],
  RIX: [56.92, 23.97], RUN: [-20.89, 55.51], SDQ: [18.43, -69.67], SEA: [47.45, -122.31],
  SEZ: [-4.67, 55.52], SFO: [37.62, -122.38], SID: [16.74, -22.95], SIN: [1.36, 103.99],
  SJO: [9.99, -84.21], SJU: [18.44, -66.00], SFJ: [67.02, -50.69], STO: [59.65, 17.92],
  SYD: [-33.94, 151.18], TFN: [28.48, -16.34], TFS: [28.04, -16.57], TLV: [32.01, 34.89],
  TPE: [25.08, 121.23], VCE: [45.51, 12.35], VIE: [48.11, 16.57], YYC: [51.12, -114.01],
  YUL: [45.47, -73.74], YVR: [49.19, -123.18], YYZ: [43.68, -79.63], ZRH: [47.46, 8.55],
};
const COUNTRY_COORDS = {
  Argentina: [-34.6, -58.4], Australia: [-25.3, 133.8], Brazil: [-14.2, -51.9], Canada: [56.1, -106.3],
  "Cape Verde": [15.1, -23.6], Colombia: [4.6, -74.1], Denmark: [56.0, 10.0], France: [46.2, 2.2],
  Germany: [51.2, 10.4], Greece: [39.1, 22.9], Greenland: [71.7, -42.6], Italy: [42.8, 12.5],
  Japan: [36.2, 138.3], Latvia: [56.9, 24.1], Maldives: [3.2, 73.2], Mexico: [23.6, -102.5],
  Netherlands: [52.1, 5.3], Norway: [61.0, 8.0], Portugal: [39.4, -8.2], Qatar: [25.3, 51.2],
  Spain: [40.4, -3.7], Sweden: [60.1, 18.6], Thailand: [15.8, 101.0], "United Arab Emirates": [24.0, 54.0],
  "United Kingdom": [54.0, -2.0], "United States": [39.8, -98.6],
};
const REGION_COORDS = {
  africa: [1, 20], asia: [30, 95], australia: [-25, 134], caribbean: [18, -66],
  central_asia: [45, 68], europe: [50, 10], greenland: [71, -42], indian_ocean: [-12, 65],
  japan: [36, 138], latin_america: [-8, -65], middle_east: [26, 48], nordic: [62, 15],
  north_america: [45, -100], oceania: [-15, 160], south_america: [-15, -60], warm_europe: [39, 10],
};

const state = {
  data: null,
  selectedLeg: null,
  suggestions: [],
  activeSuggestion: -1,
  view: "cards",
  mapRows: [],
  map: null,
  markerLayer: null,
};

const els = {
  origin: document.querySelector("#origin"),
  customOrigin: document.querySelector("#customOrigin"),
  exactDestination: document.querySelector("#exactDestination"),
  destinationQuery: document.querySelector("#destinationQuery"),
  destinationSuggestions: document.querySelector("#destinationSuggestions"),
  monthPreset: document.querySelector("#monthPreset"),
  startDate: document.querySelector("#startDate"),
  endDate: document.querySelector("#endDate"),
  region: document.querySelector("#region"),
  cardsViewButton: document.querySelector("#cardsViewButton"),
  mapViewButton: document.querySelector("#mapViewButton"),
  mapPanel: document.querySelector("#mapPanel"),
  worldMap: document.querySelector("#worldMap"),
  mapMeta: document.querySelector("#mapMeta"),
  resetMapButton: document.querySelector("#resetMapButton"),
  mapSheet: document.querySelector("#mapSheet"),
  mapSheetContent: document.querySelector("#mapSheetContent"),
  maxHours: document.querySelector("#maxHours"),
  maxHoursLabel: document.querySelector("#maxHoursLabel"),
  maxStops: document.querySelector("#maxStops"),
  sortMode: document.querySelector("#sortMode"),
  resetButton: document.querySelector("#resetButton"),
  exportButton: document.querySelector("#exportButton"),
  importButton: document.querySelector("#importButton"),
  importFile: document.querySelector("#importFile"),
  routesButton: document.querySelector("#routesButton"),
  reviewButton: document.querySelector("#reviewButton"),
  results: document.querySelector("#results"),
  resultMeta: document.querySelector("#resultMeta"),
  summaryStrip: document.querySelector("#summaryStrip"),
  dialog: document.querySelector("#checkDialog"),
  dialogTitle: document.querySelector("#dialogTitle"),
  dialogRoute: document.querySelector("#dialogRoute"),
  checkStatus: document.querySelector("#checkStatus"),
  checkNotes: document.querySelector("#checkNotes"),
  saveCheckButton: document.querySelector("#saveCheckButton"),
  routesDialog: document.querySelector("#routesDialog"),
  reviewDialog: document.querySelector("#reviewDialog"),
  routeOrigin: document.querySelector("#routeOrigin"),
  routeDestination: document.querySelector("#routeDestination"),
  routeAirline: document.querySelector("#routeAirline"),
  routeDuration: document.querySelector("#routeDuration"),
  addRouteButton: document.querySelector("#addRouteButton"),
  exportRoutesButton: document.querySelector("#exportRoutesButton"),
  routeList: document.querySelector("#routeList"),
  reviewList: document.querySelector("#reviewList"),
};

async function loadData() {
  const [airlines, destinations, routes, availability, adapters, airports] = await Promise.all(
    Object.values(DATA_PATHS).map((path) => fetch(path).then((response) => {
      if (!response.ok) throw new Error(`Could not load ${path}`);
      return response.json();
    }))
  );
  state.data = {
    airlines: Object.fromEntries(airlines.airlines.map((item) => [item.code.toUpperCase(), item.name])),
    destinations: destinations.destinations,
    routes: routes.legs,
    initialChecks: availability.checks || [],
    adapters: adapters.adapters || {},
    airports: airports.airports || {},
  };
}

function loadManualChecks() {
  try {
    return JSON.parse(localStorage.getItem(STORAGE_KEY) || "[]");
  } catch {
    return [];
  }
}

function saveManualChecks(checks) {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(checks));
}

function loadCustomRoutes() {
  try {
    return JSON.parse(localStorage.getItem(ROUTES_STORAGE_KEY) || "[]");
  } catch {
    return [];
  }
}

function saveCustomRoutes(routes) {
  localStorage.setItem(ROUTES_STORAGE_KEY, JSON.stringify(routes));
}

function formatDuration(minutes) {
  const hours = Math.floor(minutes / 60);
  const mins = minutes % 60;
  return `${hours}h${String(mins).padStart(2, "0")}`;
}

function daysBetween(a, b) {
  const ms = 24 * 60 * 60 * 1000;
  return Math.floor((Date.parse(a) - Date.parse(b)) / ms);
}

function checkedAgeDays(check) {
  const checkedAt = check.checked_at || check.date;
  if (!checkedAt) return null;
  return Math.max(0, daysBetween(new Date().toISOString(), checkedAt));
}

function isStale(check) {
  const age = checkedAgeDays(check);
  return age !== null && age > STALE_DAYS;
}

function routeAgeDays(route) {
  if (!route.verified_at) return null;
  return Math.max(0, daysBetween(new Date().toISOString(), route.verified_at));
}

function routeFreshness(route) {
  const age = routeAgeDays(route);
  if (age === null) return { label: "Unverified", className: "fresh-unknown", ageText: "no source date" };
  if (age <= 30) return { label: "Fresh", className: "fresh-good", ageText: `${age}d old` };
  if (age <= 90) return { label: "Aging", className: "fresh-aging", ageText: `${age}d old` };
  return { label: "Stale", className: "fresh-stale", ageText: `${age}d old` };
}

function airportCode(value) {
  const code = String(value || "").trim().toUpperCase();
  return /^[A-Z0-9]{3}$/.test(code) ? code : "";
}

function getFilters() {
  const exactDestination = airportCode(els.exactDestination.value);
  return {
    origin: airportCode(els.customOrigin.value) || els.origin.value,
    exactDestination,
    destinationQuery: els.destinationQuery.value.trim().toLowerCase(),
    start: els.startDate.value,
    end: els.endDate.value,
    region: els.region.value,
    maxMinutes: Number(els.maxHours.value) * 60,
    maxStops: Number(els.maxStops.value),
    sortMode: els.sortMode.value,
  };
}

function destinationMatchesQuery(item, query) {
  if (!query) return true;
  const haystack = [
    item.iata,
    item.city,
    item.country,
    ...(item.regions || []),
    item.country === "Maldives" ? "maldivene" : "",
  ].join(" ").toLowerCase();
  return haystack.includes(query);
}

function normalizedText(value) {
  return String(value || "")
    .normalize("NFD")
    .replace(/[\u0300-\u036f]/g, "")
    .toLowerCase();
}

function buildDestinationSuggestions(query) {
  const normalizedQuery = normalizedText(query);
  if (!normalizedQuery) return [];
  const destinationSuggestions = state.data.destinations
    .map((item) => {
      const label = `${item.city} (${item.iata}), ${item.country}`;
      const aliases = [item.iata, item.city, item.country, ...(item.regions || [])];
      if (item.country === "Maldives") aliases.push("maldivene");
      const searchable = normalizedText(aliases.join(" "));
      if (!searchable.includes(normalizedQuery)) return null;
      const exactBoost = aliases.some((alias) => normalizedText(alias) === normalizedQuery) ? 50 : 0;
      const codeBoost = normalizedText(item.iata).startsWith(normalizedQuery) ? 30 : 0;
      const cityBoost = normalizedText(item.city).startsWith(normalizedQuery) ? 20 : 0;
      return {
        type: "destination",
        value: item.iata,
        label,
        detail: item.regions.join(" · "),
        regions: item.regions || [],
        score: exactBoost + codeBoost + cityBoost,
      };
    })
    .filter(Boolean);

  const tags = [...new Set(state.data.destinations.flatMap((item) => item.regions || []))]
    .filter((tag) => normalizedText(tag).includes(normalizedQuery))
    .map((tag) => ({
      type: "tag",
      value: tag,
      label: tag.replaceAll("_", " "),
      detail: "destination tag",
      score: normalizedText(tag).startsWith(normalizedQuery) ? 15 : 0,
    }));

  return [...destinationSuggestions, ...tags]
    .sort((a, b) => b.score - a.score || a.label.localeCompare(b.label))
    .slice(0, 7);
}

function renderDestinationSuggestions() {
  const query = els.destinationQuery.value.trim();
  state.suggestions = buildDestinationSuggestions(query);
  state.activeSuggestion = Math.min(state.activeSuggestion, state.suggestions.length - 1);
  els.destinationQuery.setAttribute("aria-expanded", state.suggestions.length ? "true" : "false");
  if (!state.suggestions.length) {
    els.destinationSuggestions.classList.remove("open");
    els.destinationSuggestions.innerHTML = "";
    return;
  }
  els.destinationSuggestions.classList.add("open");
  els.destinationSuggestions.innerHTML = state.suggestions.map((item, index) => `
    <button type="button" class="suggestion ${index === state.activeSuggestion ? "active" : ""}" data-suggestion-index="${index}" role="option">
      <strong>${item.label}</strong>
      <span>${item.detail}</span>
    </button>
  `).join("");
  document.querySelectorAll("[data-suggestion-index]").forEach((button) => {
    button.addEventListener("mousedown", (event) => {
      event.preventDefault();
      applyDestinationSuggestion(Number(button.dataset.suggestionIndex));
    });
  });
}

function preferredRegion(regions) {
  const priority = ["indian_ocean", "japan", "oceania", "australia", "caribbean", "south_america", "latin_america", "central_asia", "asia", "north_america", "middle_east", "africa", "greenland", "arctic", "azores", "warm_europe", "nordic", "europe", "island", "beach", "city", "warm"];
  return priority.find((region) => regions.includes(region)) || regions[0] || "all";
}

function applyDestinationSuggestion(index) {
  const item = state.suggestions[index];
  if (!item) return;
  els.destinationQuery.value = item.value;
  if (item.type === "tag") {
    els.region.value = item.value;
  } else if (item.regions?.length) {
    els.region.value = preferredRegion(item.regions);
  }
  state.suggestions = [];
  state.activeSuggestion = -1;
  els.destinationSuggestions.classList.remove("open");
  els.destinationSuggestions.innerHTML = "";
  els.destinationQuery.setAttribute("aria-expanded", "false");
  renderRows();
}

function destinationMap(region, query) {
  const exactDestination = airportCode(els.exactDestination.value);
  if (exactDestination) {
    const destination = state.data.destinations.find((item) => item.iata.toUpperCase() === exactDestination);
    return new Map([[
      exactDestination,
      destination || { iata: exactDestination, city: exactDestination, country: "Custom destination", regions: ["all"] },
    ]]);
  }
  const entries = state.data.destinations.filter((item) => {
    const regionMatch = region === "all" || item.regions.includes(region);
    return regionMatch && destinationMatchesQuery(item, query);
  });
  return new Map(entries.map((item) => [item.iata, item]));
}

function allLegs() {
  const eligible = state.data.airlines;
  const legs = [];
  for (const item of [...state.data.routes, ...loadCustomRoutes()]) {
    const airline = item.airline.toUpperCase();
    if (!eligible[airline]) continue;
    const leg = {
      origin: item.origin.toUpperCase(),
      destination: item.destination.toUpperCase(),
      airline,
      durationMin: Number(item.duration_min),
      confidence: item.confidence || "starter",
      sourceTier: item.source_tier || "D",
      source: item.source || "",
      sourceUrl: item.source_url || "",
      verifiedAt: item.verified_at || "",
      routeConfidence: item.route_confidence || "low",
      lastCheckStatus: item.last_check_status || "",
      lastCheckOk: item.last_check_ok,
    };
    legs.push(leg);
    legs.push({
      origin: leg.destination,
      destination: leg.origin,
      airline,
      durationMin: leg.durationMin,
      confidence: leg.confidence,
      sourceTier: leg.sourceTier,
      source: leg.source,
      sourceUrl: leg.sourceUrl,
      verifiedAt: leg.verifiedAt,
      routeConfidence: leg.routeConfidence,
      lastCheckStatus: leg.lastCheckStatus,
      lastCheckOk: leg.lastCheckOk,
    });
  }
  return legs;
}

function buildAdjacency(legs) {
  const adjacency = new Map();
  for (const leg of legs) {
    if (!adjacency.has(leg.origin)) adjacency.set(leg.origin, []);
    adjacency.get(leg.origin).push(leg);
  }
  return adjacency;
}

function findItineraries(origin, destinations, adjacency, maxStops, maxMinutes) {
  const found = [];
  const maxLegs = maxStops + 1;

  function visit(current, legs, seen, elapsed) {
    if (legs.length && destinations.has(current)) {
      found.push({
        legs,
        destination: current,
        durationMin: elapsed,
        stops: Math.max(0, legs.length - 1),
        route: [legs[0].origin, ...legs.map((leg) => leg.destination)].join("-"),
      });
    }
    if (legs.length >= maxLegs) return;
    for (const leg of adjacency.get(current) || []) {
      if (seen.has(leg.destination)) continue;
      const extra = legs.length ? leg.durationMin + LAYOVER_MIN : leg.durationMin;
      if (elapsed + extra > maxMinutes) continue;
      visit(leg.destination, [...legs, leg], new Set([...seen, leg.destination]), elapsed + extra);
    }
  }

  visit(origin, [], new Set([origin]), 0);
  return found;
}

function checkMatchesDate(check, start, end) {
  if (!check.date) return true;
  return check.date >= start && check.date <= end;
}

function checkKey(check) {
  return [
    check.date || "",
    check.origin,
    check.destination,
    check.airline,
    check.flight_number || "",
  ].join("|");
}

function mergedChecks() {
  const checks = [...state.data.initialChecks, ...loadManualChecks()];
  return [...new Map(checks.map((check) => [checkKey(check), check])).values()];
}

function checksForLeg(leg, start, end) {
  return mergedChecks()
    .filter((check) => (
      check.origin === leg.origin &&
      check.destination === leg.destination &&
      check.airline === leg.airline &&
      checkMatchesDate(check, start, end)
    ))
    .sort((a, b) => String(b.checked_at || b.date || "").localeCompare(String(a.checked_at || a.date || "")));
}

function legStatus(leg, start, end) {
  const matches = checksForLeg(leg, start, end);
  if (!matches.length) {
    return { status: "unknown", check: null, stale: false };
  }
  const check = matches[0];
  return { status: check.status || "unknown", check, stale: isStale(check) };
}

function legStatusesForItinerary(itinerary, start, end) {
  return itinerary.legs.map((leg) => ({ leg, ...legStatus(leg, start, end) }));
}

function statusForItinerary(legStatuses) {
  const statuses = legStatuses.map((item) => item.status);
  if (statuses.includes("none")) return "none";
  if (statuses.includes("some")) return "some";
  if (statuses.length && statuses.every((status) => status === "9plus")) return "9plus";
  return "unknown";
}

function routeQualityForItinerary(itinerary, alternativesCount) {
  if (itinerary.stops === 0 && alternativesCount >= 2) {
    return { label: "Strong", className: "outlook-green", reason: "Direct option and multiple route alternatives" };
  }
  if (itinerary.stops === 0) {
    return { label: "Good", className: "outlook-green", reason: "Direct option" };
  }
  if (itinerary.stops === 1 && alternativesCount >= 3) {
    return { label: "Good", className: "outlook-green", reason: "One stop with several backup routes" };
  }
  if (itinerary.stops <= 1) {
    return { label: "Explore", className: "outlook-yellow", reason: "Plausible route, verify dates and connection" };
  }
  return { label: "Fragile", className: "outlook-red", reason: "Longer multi-stop route, backup needed" };
}

function loadNoteForItinerary(itinerary, status, legStatuses) {
  const stale = legStatuses.some((item) => item.stale);
  if (status === "none") return stale ? "Load note: none, stale" : "Load note: none";
  if (status === "some") return stale ? "Load note: some, stale" : "Load note: some";
  if (status === "9plus") return stale ? "Load note: 9+, stale" : "Load note: 9+";
  return "Load not checked";
}

function scoreItinerary(itinerary, status, routeQuality, alternativesCount) {
  let score = 1000 - itinerary.durationMin - itinerary.stops * 120;
  if (new Set(itinerary.legs.map((leg) => leg.airline)).size === 1) score += 40;
  score += Math.min(alternativesCount, 8) * 35;
  if (routeQuality.label === "Strong") score += 220;
  if (routeQuality.label === "Good") score += 140;
  if (routeQuality.label === "Explore") score += 40;
  if (routeQuality.label === "Fragile") score -= 220;
  if (status === "9plus") score += 40;
  if (status === "some") score += 60;
  if (status === "none") score -= 400;
  return score;
}

function bestReturnItinerary(itinerary, origin, adjacency, maxStops, maxMinutes) {
  return findItineraries(itinerary.destination, new Set([origin]), adjacency, maxStops, maxMinutes)
    .sort((a, b) => a.durationMin - b.durationMin || a.stops - b.stops)[0] || null;
}

function buildRows() {
  const filters = getFilters();
  const destinations = destinationMap(filters.region, filters.destinationQuery);
  const legs = allLegs();
  const adjacency = buildAdjacency(legs);
  const candidates = findItineraries(filters.origin, new Set(destinations.keys()), adjacency, filters.maxStops, filters.maxMinutes);
  const baseRows = candidates
    .map((itinerary) => {
      const returnItinerary = bestReturnItinerary(itinerary, filters.origin, adjacency, filters.maxStops, filters.maxMinutes);
      if (!returnItinerary) return null;
      const legStatuses = legStatusesForItinerary(itinerary, filters.start, filters.end);
      const status = statusForItinerary(legStatuses);
      return {
        itinerary,
        returnItinerary,
        status,
        legStatuses,
        destination: destinations.get(itinerary.destination),
      };
    })
    .filter(Boolean);
  const alternatives = new Map();
  for (const row of baseRows) {
    alternatives.set(row.itinerary.destination, (alternatives.get(row.itinerary.destination) || 0) + 1);
  }
  const rows = baseRows.map((row) => {
    const alternativesCount = alternatives.get(row.itinerary.destination) || 1;
    const routeQuality = routeQualityForItinerary(row.itinerary, alternativesCount);
    return {
      ...row,
      alternativesCount,
      routeQuality,
      loadNote: loadNoteForItinerary(row.itinerary, row.status, row.legStatuses),
      score: scoreItinerary(row.itinerary, row.status, routeQuality, alternativesCount),
    };
  });

  rows.sort((a, b) => {
    if (filters.sortMode === "duration") return a.itinerary.durationMin - b.itinerary.durationMin;
    if (filters.sortMode === "route") return b.score - a.score || b.alternativesCount - a.alternativesCount;
    if (filters.sortMode === "status") {
      const rank = { "9plus": 0, some: 1, unknown: 2, none: 3 };
      return rank[a.status] - rank[b.status] || a.itinerary.durationMin - b.itinerary.durationMin;
    }
    return b.score - a.score || a.itinerary.durationMin - b.itinerary.durationMin;
  });
  return rows;
}

function destinationCoordinates(destination) {
  if (!destination) return null;
  const code = destination.iata?.toUpperCase();
  const airport = state.data.airports[code];
  if (airport) return [airport.lat, airport.lon];
  if (COUNTRY_COORDS[destination.country]) return COUNTRY_COORDS[destination.country];
  for (const region of destination.regions || []) {
    if (REGION_COORDS[region]) return REGION_COORDS[region];
  }
  return null;
}

function bestRowsByDestination(rows) {
  const best = new Map();
  for (const row of rows) {
    const current = best.get(row.itinerary.destination);
    if (!current || row.score > current.score || (
      row.score === current.score && row.itinerary.durationMin < current.itinerary.durationMin
    )) {
      best.set(row.itinerary.destination, row);
    }
  }
  return [...best.values()];
}

function timeAtDestinationText(row, filters) {
  const start = Date.parse(filters.start);
  const end = Date.parse(filters.end);
  if (!Number.isFinite(start) || !Number.isFinite(end) || end < start) return "Unknown";
  const windowMinutes = Math.max(0, (end - start) / 60000);
  const travelMinutes = row.itinerary.durationMin + (row.returnItinerary?.durationMin || row.itinerary.durationMin);
  const destinationMinutes = Math.max(0, windowMinutes - travelMinutes);
  const days = Math.floor(destinationMinutes / 1440);
  const hours = Math.floor((destinationMinutes % 1440) / 60);
  return `${days}d ${hours}h`;
}

function formatDateTime(value) {
  if (!Number.isFinite(value)) return "Unknown";
  const date = new Date(value);
  const datePart = date.toLocaleDateString("nb-NO", {
    day: "2-digit",
    month: "2-digit",
    year: "numeric",
  });
  const timePart = date.toLocaleTimeString("nb-NO", {
    hour: "2-digit",
    minute: "2-digit",
  });
  return `${datePart} ${timePart}`;
}

function formatDate(value) {
  const parsed = Date.parse(value);
  if (!Number.isFinite(parsed)) return value || "Unknown";
  return new Date(parsed).toLocaleDateString("nb-NO", {
    day: "2-digit",
    month: "2-digit",
    year: "numeric",
  });
}

function returnTiming(row, filters) {
  const end = Date.parse(filters.end);
  if (!Number.isFinite(end) || !row.returnItinerary) {
    return { leaveDestination: "Unknown", homeBy: filters.end || "Unknown" };
  }
  return {
    leaveDestination: formatDateTime(end - row.returnItinerary.durationMin * 60000),
    homeBy: formatDateTime(end),
  };
}

function dateWindowText(filters) {
  if (!filters.start || !filters.end) return "Custom window";
  return `${formatDate(filters.start)} to ${formatDate(filters.end)}`;
}

function routeAirlinesText(row) {
  return row.itinerary.legs
    .map((leg) => `${leg.airline} ${state.data.airlines[leg.airline] || ""}`.trim())
    .filter((value, index, list) => list.indexOf(value) === index)
    .join(" + ");
}

function legListHtml(itinerary) {
  return itinerary.legs.map((leg) => {
    const airline = state.data.airlines[leg.airline] || leg.airline;
    return `
      <div class="map-leg">
        <strong>${leg.origin}-${leg.destination} ${leg.airline}</strong>
        <span>${airline} · ${formatDuration(leg.durationMin)}</span>
      </div>
    `;
  }).join("");
}

function mapSheetRoute(row, filters) {
  const timing = returnTiming(row, filters);
  const returnItinerary = row.returnItinerary;
  return `
    <article class="map-route">
      <div class="map-route-head">
        <div>
          <strong>${row.destination.city} (${row.itinerary.destination})</strong>
          <span>${row.destination.country}</span>
        </div>
        <span class="outlook-pill ${row.routeQuality.className}">${row.routeQuality.label}</span>
      </div>
      <div class="map-stats">
        <div><strong>${formatDuration(row.itinerary.durationMin)}</strong><span>outbound</span></div>
        <div><strong>${formatDuration(returnItinerary.durationMin)}</strong><span>return</span></div>
        <div><strong>${timeAtDestinationText(row, filters)}</strong><span>there</span></div>
        <div><strong>${row.alternativesCount}</strong><span>routes</span></div>
      </div>
      <div class="map-return-window">
        <div><strong>Leave destination by</strong><span>${timing.leaveDestination}</span></div>
        <div><strong>Home by</strong><span>${timing.homeBy}</span></div>
      </div>
      <p class="map-subhead">Outbound</p>
      <div class="map-route-line">${row.itinerary.route}</div>
      <div class="map-airlines">${routeAirlinesText(row)}</div>
      <div class="map-leg-list">${legListHtml(row.itinerary)}</div>
      <p class="map-subhead">Return</p>
      <div class="map-route-line">${returnItinerary.route}</div>
      <div class="map-leg-list">${legListHtml(returnItinerary)}</div>
      <div class="map-note">${row.routeQuality.reason} · ${row.loadNote} · times are rough block-time estimates</div>
      <button type="button" class="map-full-button" data-show-destination="${row.itinerary.destination}">Show full route info</button>
    </article>
  `;
}

function ensureLeafletMap() {
  if (!window.L) {
    els.worldMap.innerHTML = `<div class="empty">Map library could not load. Check internet access and refresh.</div>`;
    return false;
  }
  if (state.map) return true;
  state.map = L.map(els.worldMap, {
    worldCopyJump: true,
    zoomControl: true,
    attributionControl: true,
  }).setView([25, 10], 2);
  L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
    maxZoom: 10,
    attribution: "&copy; OpenStreetMap contributors",
  }).addTo(state.map);
  state.markerLayer = L.markerClusterGroup
    ? L.markerClusterGroup({ showCoverageOnHover: false, maxClusterRadius: 42 })
    : L.layerGroup();
  state.markerLayer.addTo(state.map);
  return true;
}

function renderMap(rows) {
  const filters = getFilters();
  if (!ensureLeafletMap()) return;
  state.markerLayer.clearLayers();
  const mappedRows = bestRowsByDestination(rows)
    .map((row) => ({ row, coords: destinationCoordinates(row.destination) }))
    .filter((item) => item.coords);
  const mappedCount = mappedRows.length;
  els.mapMeta.textContent = `${mappedCount} mapped destination${mappedCount === 1 ? "" : "s"} from ${filters.origin}`;
  for (const { row, coords } of mappedRows) {
    const marker = L.circleMarker(coords, {
      radius: 8,
      color: "#ffffff",
      weight: 2,
      fillColor: "#0f766e",
      fillOpacity: 0.92,
    });
    marker.bindTooltip(`${row.destination.city} (${row.itinerary.destination})`, { direction: "top" });
    marker.on("click", () => openMapSheet([row]));
    state.markerLayer.addLayer(marker);
  }
  if (mappedRows.length) {
    const bounds = L.latLngBounds(mappedRows.map((item) => item.coords));
    state.map.fitBounds(bounds.pad(0.18), { maxZoom: 4 });
  } else {
    state.map.setView([25, 10], 2);
  }
  window.setTimeout(() => {
    state.map.invalidateSize();
  });
}

function openMapSheet(rows) {
  const filters = getFilters();
  const sorted = [...rows].sort((a, b) => b.score - a.score || a.itinerary.durationMin - b.itinerary.durationMin);
  const first = sorted[0];
  const title = rows.length === 1
    ? `${first.destination.city} (${first.itinerary.destination})`
    : `${rows.length} destinations`;
  els.mapSheetContent.innerHTML = `
    <div class="map-sheet-head">
      <div>
        <p class="eyebrow">Map selection</p>
        <h2>${title}</h2>
        <p class="muted">${dateWindowText(filters)} · from ${filters.origin}</p>
      </div>
      <button type="button" data-close-map-sheet>Close</button>
    </div>
    <div class="map-sheet-list">
      ${sorted.slice(0, 6).map((row) => mapSheetRoute(row, filters)).join("")}
    </div>
  `;
  els.mapSheet.hidden = false;
  els.mapSheet.querySelector("[data-close-map-sheet]").addEventListener("click", closeMapSheet);
  els.mapSheet.querySelectorAll("[data-show-destination]").forEach((button) => {
    button.addEventListener("click", () => {
      showCardsView();
      closeMapSheet();
      window.setTimeout(() => {
        document.querySelector(`[data-card-destination="${button.dataset.showDestination}"]`)?.scrollIntoView({
          behavior: "smooth",
          block: "start",
        });
      }, 50);
    });
  });
}

function closeMapSheet() {
  els.mapSheet.hidden = true;
  els.mapSheetContent.innerHTML = "";
}

function showCardsView() {
  state.view = "cards";
  els.cardsViewButton.classList.add("active");
  els.mapViewButton.classList.remove("active");
  els.mapPanel.hidden = true;
  els.results.hidden = false;
}

function showMapView() {
  state.view = "map";
  els.mapViewButton.classList.add("active");
  els.cardsViewButton.classList.remove("active");
  els.results.hidden = true;
  els.mapPanel.hidden = false;
  renderMap(state.mapRows);
}

function renderSummary(rows) {
  const destinations = new Set(rows.map((row) => row.itinerary.destination)).size;
  const strong = rows.filter((row) => row.routeQuality.label === "Strong" || row.routeQuality.label === "Good").length;
  const customRoutes = loadCustomRoutes().length;
  els.summaryStrip.innerHTML = `
    <div class="metric"><strong>${rows.length}</strong><span>candidates</span></div>
    <div class="metric"><strong>${destinations}</strong><span>destinations</span></div>
    <div class="metric"><strong>${strong}/${customRoutes}</strong><span>good routes / custom</span></div>
  `;
}

function renderRows() {
  if (!state.data) return;
  els.maxHoursLabel.textContent = els.maxHours.value;
  const rows = buildRows();
  state.mapRows = rows;
  renderSummary(rows);
  if (state.view === "map") renderMap(rows);
  const filters = getFilters();
  const queryText = filters.exactDestination
    ? ` to ${filters.exactDestination}`
    : filters.destinationQuery
      ? ` matching "${filters.destinationQuery}"`
      : "";
  els.resultMeta.textContent = `${rows.length} route candidates from ${filters.origin}${queryText}. Starter route map, not live schedules.`;

  if (!rows.length) {
    els.results.innerHTML = `<div class="empty">No candidates match these filters yet. Try more stops, more hours, or a broader region.</div>`;
    if (state.view === "map") {
      els.worldMap.innerHTML = `<div class="empty">No mapped candidates match these filters yet.</div>`;
      els.mapMeta.textContent = "No mapped destinations";
    }
    return;
  }

  els.results.innerHTML = rows.slice(0, 40).map((row, index) => renderCard(row, index)).join("");
  document.querySelectorAll("[data-check-leg]").forEach((button) => {
    button.addEventListener("click", () => openCheckDialog(JSON.parse(button.dataset.checkLeg)));
  });
  document.querySelectorAll("[data-open-check]").forEach((button) => {
    button.addEventListener("click", () => openAvailabilityCheck(JSON.parse(button.dataset.openCheck)));
  });
}

function renderCard(row, index) {
  const { itinerary, destination, status, routeQuality, legStatuses, alternativesCount, loadNote } = row;
  const statusClass = STATUS_CLASSES[status];
  const legs = legStatuses.map(({ leg, status: itemStatus, check, stale }) => {
    const airline = state.data.airlines[leg.airline] || leg.airline;
    const adapter = state.data.adapters[leg.airline] || state.data.adapters.default || {};
    const freshness = routeFreshness({ verified_at: leg.verifiedAt });
    const lastCheckText = leg.lastCheckOk === false && leg.lastCheckStatus ? ` · last check: ${leg.lastCheckStatus}` : "";
    const payload = JSON.stringify(leg).replaceAll("\"", "&quot;");
    const adapterPayload = JSON.stringify({
      ...leg,
      url: adapter.url || "",
      instructions: adapter.instructions || "",
    }).replaceAll("\"", "&quot;");
    const age = check ? checkedAgeDays(check) : null;
    const statusLabel = STATUS_LABELS[itemStatus] || "Unknown";
    const staleText = stale ? " · stale" : "";
    const checkText = check ? `${statusLabel}${age === null ? "" : ` · ${age}d ago`}${staleText}` : "Not checked";
    const sourceText = adapter.mode ? `${adapter.mode.replace("_", " ")} · ${adapter.supports_9_pax || "unknown"} 9-pax` : "manual search";
    const openButton = adapter.url ? `<button type="button" data-open-check="${adapterPayload}">Open check</button>` : "";
    return `
      <div class="leg">
        <div>
          <div class="leg-code">${leg.origin}-${leg.destination} ${leg.airline}</div>
          <div class="leg-airline">${airline} · ${sourceText}</div>
        </div>
        <div>
          <div class="leg-duration">${formatDuration(leg.durationMin)} block estimate</div>
          <div class="leg-check ${stale ? "stale" : ""}">${checkText}</div>
          <div class="freshness ${freshness.className}">${freshness.label} · ${freshness.ageText} · tier ${leg.sourceTier}${lastCheckText}</div>
        </div>
        <div class="leg-actions">
          ${openButton}
          <button type="button" data-check-leg="${payload}">Record</button>
        </div>
      </div>
    `;
  }).join("");

  return `
    <article class="card" data-card-destination="${itinerary.destination}">
      <div class="card-head">
        <div>
          <div class="destination">
            <h3>${index + 1}. ${destination.city}</h3>
            <span>${itinerary.destination}, ${destination.country}</span>
          </div>
          <p class="route-line">${itinerary.route}</p>
        </div>
        <div class="pill-stack">
          <span class="outlook-pill ${routeQuality.className}">${routeQuality.label}</span>
          <span class="status-pill ${statusClass}">${STATUS_LABELS[status]}</span>
        </div>
      </div>
      <div class="legs">${legs}</div>
      <div class="card-meta">
        ${routeQuality.reason} · ${alternativesCount} route alternative${alternativesCount === 1 ? "" : "s"} to ${itinerary.destination} · ${loadNote} · one-way estimate ${formatDuration(itinerary.durationMin)} with assumed ${LAYOVER_MIN}m layover(s)
      </div>
    </article>
  `;
}

function openAvailabilityCheck(payload) {
  if (payload.instructions) {
    navigator.clipboard?.writeText(payload.instructions).catch(() => {});
  }
  window.open(payload.url, "_blank", "noopener,noreferrer");
}

function openCheckDialog(leg) {
  state.selectedLeg = leg;
  els.dialogTitle.textContent = `${leg.origin}-${leg.destination} ${leg.airline}`;
  els.dialogRoute.textContent = `Record your manual 9-adult booking-site indication for ${els.startDate.value}.`;
  els.checkStatus.value = "9plus";
  els.checkNotes.value = "";
  els.dialog.showModal();
}

function saveSelectedCheck() {
  if (!state.selectedLeg) return;
  const leg = state.selectedLeg;
  const checks = loadManualChecks();
  const entry = {
    origin: leg.origin,
    destination: leg.destination,
    airline: leg.airline,
    date: els.startDate.value,
    status: els.checkStatus.value,
    source: "manual 9-pax airline website check",
    confidence: "manual",
    checked_at: new Date().toISOString(),
    notes: els.checkNotes.value.trim(),
  };
  const key = checkKey(entry);
  const index = checks.findIndex((check) => checkKey(check) === key);
  if (index >= 0) checks[index] = entry;
  else checks.push(entry);
  saveManualChecks(checks);
  state.selectedLeg = null;
  renderRows();
}

function exportChecks() {
  const checks = loadManualChecks();
  const payload = JSON.stringify({ exported_at: new Date().toISOString(), checks }, null, 2);
  const blob = new Blob([payload], { type: "application/json" });
  const url = URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.href = url;
  link.download = "manual_9pax_checks.json";
  link.click();
  URL.revokeObjectURL(url);
}

function importChecks(file) {
  if (!file) return;
  const reader = new FileReader();
  reader.addEventListener("load", () => {
    try {
      const parsed = JSON.parse(String(reader.result));
      const incoming = Array.isArray(parsed) ? parsed : parsed.checks;
      if (!Array.isArray(incoming)) throw new Error("JSON must contain a checks array");
      const existing = loadManualChecks();
      const merged = [...existing, ...incoming]
        .filter((check) => check.origin && check.destination && check.airline && check.date && check.status)
        .map((check) => ({
          ...check,
          origin: check.origin.toUpperCase(),
          destination: check.destination.toUpperCase(),
          airline: check.airline.toUpperCase(),
        }));
      saveManualChecks([...new Map(merged.map((check) => [checkKey(check), check])).values()]);
      els.importFile.value = "";
      renderRows();
    } catch (error) {
      alert(`Could not import checks: ${error.message}`);
    }
  });
  reader.readAsText(file);
}

function routeKey(route) {
  return [route.origin, route.destination, route.airline].join("|");
}

function openRoutesDialog() {
  renderRouteList();
  els.routeOrigin.value = getFilters().origin;
  els.routeDestination.value = "";
  els.routeAirline.value = "";
  els.routeDuration.value = "";
  els.routesDialog.showModal();
}

function addCustomRoute() {
  const route = {
    origin: els.routeOrigin.value.trim().toUpperCase(),
    destination: els.routeDestination.value.trim().toUpperCase(),
    airline: els.routeAirline.value.trim().toUpperCase(),
    duration_min: Number(els.routeDuration.value),
    confidence: "custom",
  };
  if (route.origin.length !== 3 || route.destination.length !== 3) {
    alert("Origin and destination must be 3-letter airport codes.");
    return;
  }
  if (route.airline.length < 2) {
    alert("Airline code must be at least 2 characters.");
    return;
  }
  if (!Number.isFinite(route.duration_min) || route.duration_min < 20) {
    alert("Duration must be at least 20 minutes.");
    return;
  }
  if (!state.data.airlines[route.airline]) {
    alert(`${route.airline} is not in the eligible airline list yet.`);
    return;
  }
  const routes = loadCustomRoutes();
  const key = routeKey(route);
  const index = routes.findIndex((item) => routeKey(item) === key);
  if (index >= 0) routes[index] = route;
  else routes.push(route);
  routes.sort((a, b) => routeKey(a).localeCompare(routeKey(b)));
  saveCustomRoutes(routes);
  renderRouteList();
  renderRows();
  els.routeDestination.value = "";
  els.routeDuration.value = "";
}

function deleteCustomRoute(key) {
  saveCustomRoutes(loadCustomRoutes().filter((route) => routeKey(route) !== key));
  renderRouteList();
  renderRows();
}

function renderRouteList() {
  const customRoutes = loadCustomRoutes();
  if (!customRoutes.length) {
    els.routeList.innerHTML = `<div class="empty compact">No custom routes yet.</div>`;
    return;
  }
  els.routeList.innerHTML = customRoutes.map((route) => {
    const key = routeKey(route);
    const airline = state.data.airlines[route.airline] || route.airline;
    return `
      <div class="route-row">
        <div>
          <strong>${route.origin}-${route.destination} ${route.airline}</strong>
          <span>${airline} · ${formatDuration(Number(route.duration_min))}</span>
        </div>
        <button type="button" data-delete-route="${key}">Remove</button>
      </div>
    `;
  }).join("");
  document.querySelectorAll("[data-delete-route]").forEach((button) => {
    button.addEventListener("click", () => deleteCustomRoute(button.dataset.deleteRoute));
  });
}

function routesNeedingReview() {
  return state.data.routes
    .map((route) => ({ ...route, freshness: routeFreshness(route) }))
    .filter((route) => route.freshness.label !== "Fresh")
    .sort((a, b) => {
      const rank = { Unverified: 0, Stale: 1, Aging: 2 };
      return (rank[a.freshness.label] ?? 9) - (rank[b.freshness.label] ?? 9)
        || a.origin.localeCompare(b.origin)
        || a.destination.localeCompare(b.destination);
    });
}

function openReviewDialog() {
  const routes = routesNeedingReview();
  if (!routes.length) {
    els.reviewList.innerHTML = `<div class="empty compact">All starter routes are fresh.</div>`;
  } else {
    els.reviewList.innerHTML = routes.slice(0, 80).map((route) => {
      const airline = state.data.airlines[route.airline] || route.airline;
      const sourceLink = route.source_url ? `<a href="${route.source_url}" target="_blank" rel="noreferrer">source</a>` : "no source";
      return `
        <div class="route-row">
          <div>
            <strong>${route.origin}-${route.destination} ${route.airline}</strong>
            <span>${airline} · ${route.freshness.label} · ${route.freshness.ageText} · tier ${route.source_tier || "D"} · ${route.route_confidence || "low"} confidence · ${sourceLink}</span>
          </div>
        </div>
      `;
    }).join("");
  }
  els.reviewDialog.showModal();
}

function exportRoutes() {
  const routes = loadCustomRoutes();
  const payload = JSON.stringify({ exported_at: new Date().toISOString(), routes }, null, 2);
  const blob = new Blob([payload], { type: "application/json" });
  const url = URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.href = url;
  link.download = "custom_routes.json";
  link.click();
  URL.revokeObjectURL(url);
}

function bindEvents() {
  [els.origin, els.customOrigin, els.exactDestination, els.destinationQuery, els.startDate, els.endDate, els.region, els.maxHours, els.maxStops, els.sortMode]
    .forEach((control) => control.addEventListener("input", renderRows));
  [els.customOrigin, els.exactDestination].forEach((control) => {
    control.addEventListener("input", () => {
      control.value = control.value.toUpperCase().replace(/[^A-Z0-9]/g, "").slice(0, 3);
    });
  });
  els.destinationQuery.addEventListener("input", () => {
    state.activeSuggestion = -1;
    renderDestinationSuggestions();
  });
  els.destinationQuery.addEventListener("focus", renderDestinationSuggestions);
  els.destinationQuery.addEventListener("blur", () => {
    window.setTimeout(() => {
      els.destinationSuggestions.classList.remove("open");
      els.destinationQuery.setAttribute("aria-expanded", "false");
    }, 120);
  });
  els.destinationQuery.addEventListener("keydown", (event) => {
    if (!state.suggestions.length) return;
    if (event.key === "ArrowDown") {
      event.preventDefault();
      state.activeSuggestion = (state.activeSuggestion + 1) % state.suggestions.length;
      renderDestinationSuggestions();
    }
    if (event.key === "ArrowUp") {
      event.preventDefault();
      state.activeSuggestion = (state.activeSuggestion - 1 + state.suggestions.length) % state.suggestions.length;
      renderDestinationSuggestions();
    }
    if (event.key === "Enter" && state.activeSuggestion >= 0) {
      event.preventDefault();
      applyDestinationSuggestion(state.activeSuggestion);
    }
    if (event.key === "Escape") {
      state.suggestions = [];
      state.activeSuggestion = -1;
      renderDestinationSuggestions();
    }
  });
  els.monthPreset.addEventListener("input", () => {
    if (!els.monthPreset.value) return;
    const [start, end] = els.monthPreset.value.split("|");
    els.startDate.value = start;
    els.endDate.value = end;
    renderRows();
  });
  els.resetButton.addEventListener("click", () => {
    els.origin.value = "OSL";
    els.customOrigin.value = "";
    els.exactDestination.value = "";
    els.destinationQuery.value = "";
    els.monthPreset.value = "";
    els.startDate.value = "2026-11-04";
    els.endDate.value = "2026-11-12";
    els.region.value = "warm_europe";
    els.maxHours.value = "24";
    els.maxStops.value = "1";
    els.sortMode.value = "recommended";
    renderRows();
  });
  els.exportButton.addEventListener("click", exportChecks);
  els.importButton.addEventListener("click", () => els.importFile.click());
  els.importFile.addEventListener("change", () => importChecks(els.importFile.files[0]));
  els.cardsViewButton.addEventListener("click", showCardsView);
  els.mapViewButton.addEventListener("click", showMapView);
  els.resetMapButton.addEventListener("click", () => {
    els.region.value = "all";
    els.exactDestination.value = "";
    els.destinationQuery.value = "";
    closeMapSheet();
    renderRows();
  });
  els.saveCheckButton.addEventListener("click", saveSelectedCheck);
  els.routesButton.addEventListener("click", openRoutesDialog);
  els.reviewButton.addEventListener("click", openReviewDialog);
  els.addRouteButton.addEventListener("click", addCustomRoute);
  els.exportRoutesButton.addEventListener("click", exportRoutes);
}

async function init() {
  bindEvents();
  try {
    await loadData();
    renderRows();
  } catch (error) {
    els.resultMeta.textContent = "Could not load local data.";
    els.results.innerHTML = `<div class="empty">${error.message}. Start a local server from this folder and refresh.</div>`;
  }
}

init();
