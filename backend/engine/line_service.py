import csv
import zipfile

_line_cache = None


def load_line_index():
    global _line_cache

    if _line_cache is not None:
        return _line_cache

    print("Loading line index...")

    with zipfile.ZipFile("data/PID_GTFS.zip") as z:
        stops = {}
        routes = {}
        trips = {}
        stop_times_by_trip = {}

        with z.open("stops.txt") as f:
            reader = csv.DictReader((line.decode("utf-8") for line in f))
            for row in reader:
                stops[row["stop_id"]] = {
                    "id": row["stop_id"],
                    "name": row["stop_name"],
                    "lat": row["stop_lat"],
                    "lon": row["stop_lon"],
                }

        with z.open("routes.txt") as f:
            reader = csv.DictReader((line.decode("utf-8") for line in f))
            for row in reader:
                routes[row["route_id"]] = {
                    "line": row["route_short_name"],
                    "type": row["route_type"],
                }

        with z.open("trips.txt") as f:
            reader = csv.DictReader((line.decode("utf-8") for line in f))
            for row in reader:
                trips[row["trip_id"]] = row["route_id"]

        with z.open("stop_times.txt") as f:
            reader = csv.DictReader((line.decode("utf-8") for line in f))
            for row in reader:
                trip_id = row["trip_id"]
                stop_id = row["stop_id"]

                if stop_id not in stops:
                    continue

                stop_times_by_trip.setdefault(trip_id, []).append(
                    {
                        "stop_id": stop_id,
                        "sequence": int(row["stop_sequence"]),
                    }
                )

    _line_cache = {
        "stops": stops,
        "routes": routes,
        "trips": trips,
        "stop_times_by_trip": stop_times_by_trip,
    }

    print("Line index loaded.")
    return _line_cache


def get_line(line: str):
    data = load_line_index()

    best_trip_stops = []

    for trip_id, route_id in data["trips"].items():
        route = data["routes"].get(route_id)

        if not route:
            continue

        if route["line"] != line:
            continue

        trip_stops = data["stop_times_by_trip"].get(trip_id, [])

        if len(trip_stops) > len(best_trip_stops):
            best_trip_stops = trip_stops

    best_trip_stops = sorted(best_trip_stops, key=lambda item: item["sequence"])

    stops = []

    for item in best_trip_stops:
        stop = data["stops"].get(item["stop_id"])

        if not stop:
            continue

        stops.append(stop)

    return {
        "line": line,
        "stops": stops,
    }