import csv
import zipfile

_services = None


def route_type_to_mode(route_type, short_name):
    short_name = str(short_name).strip().upper()

    if short_name in ["A", "B", "C"]:
        return "metro"

    if route_type == "1":
        return "metro"

    if route_type == "0":
        return "tram"

    if route_type == "2":
        return "train"

    if route_type == "3":
        return "bus"

    return "bus"


def load_services():
    global _services

    if _services is not None:
        return _services

    print("Loading GTFS services...")

    services = {}

    with zipfile.ZipFile("data/PID_GTFS.zip") as z:
        stops = {}
        parent_by_stop = {}

        with z.open("stops.txt") as f:
            reader = csv.DictReader((line.decode("utf-8") for line in f))

            for row in reader:
                stop_id = row["stop_id"]
                parent_station = row.get("parent_station") or ""

                stops[stop_id] = {
                    "name": row["stop_name"],
                    "parent": parent_station,
                }

                if parent_station:
                    parent_by_stop[stop_id] = parent_station

        routes = {}

        with z.open("routes.txt") as f:
            reader = csv.DictReader((line.decode("utf-8") for line in f))

            for row in reader:
                routes[row["route_id"]] = {
                    "short": row["route_short_name"],
                    "type": row["route_type"],
                }

        trips = {}

        with z.open("trips.txt") as f:
            reader = csv.DictReader((line.decode("utf-8") for line in f))

            for row in reader:
                trips[row["trip_id"]] = row["route_id"]

        with z.open("stop_times.txt") as f:
            reader = csv.DictReader((line.decode("utf-8") for line in f))

            for row in reader:
                stop_id = row["stop_id"]
                trip_id = row["trip_id"]

                if trip_id not in trips:
                    continue

                route_id = trips[trip_id]

                if route_id not in routes:
                    continue

                route = routes[route_id]
                short_name = route["short"]
                route_type = route["type"]

                item = (short_name, route_type)

                services.setdefault(stop_id, set()).add(item)

                parent_id = parent_by_stop.get(stop_id)

                if parent_id:
                    services.setdefault(parent_id, set()).add(item)

    _services = services

    print("Services loaded.")
    return services


def get_services(stop_id: str):
    services = load_services()
    raw_services = services.get(stop_id, set())

    result = {
        "metro": [],
        "tram": [],
        "bus": [],
        "train": [],
    }

    for short_name, route_type in raw_services:
        mode = route_type_to_mode(route_type, short_name)

        if short_name and short_name not in result[mode]:
            result[mode].append(short_name)

    for mode in result:
        result[mode].sort(key=lambda value: (len(value), value))

    return {
        mode: lines
        for mode, lines in result.items()
        if len(lines) > 0
    }