from typing import Optional
from fastapi import APIRouter
from fastapi.responses import JSONResponse
import zipfile
import csv
import math

from engine.services import get_services

router = APIRouter()
cached_stops = None


def guess_modes_from_services(services):
    modes = []

    if services.get("metro"):
        modes.append("metro")
    if services.get("tram"):
        modes.append("tram")
    if services.get("bus"):
        modes.append("bus")
    if services.get("train"):
        modes.append("train")

    if not modes:
        modes.append("bus")

    return modes


def is_hub(stop_name: str):
    hubs = [
        "muzeum",
        "můstek",
        "florenc",
        "anděl",
        "náměstí míru",
        "hlavní nádraží",
        "dejvická",
        "černý most",
        "zličín",
        "letňany",
    ]

    return stop_name.lower() in hubs


def calculate_distance_m(lat1, lon1, lat2, lon2):
    earth_radius_m = 6371000

    lat1_rad = math.radians(float(lat1))
    lon1_rad = math.radians(float(lon1))
    lat2_rad = math.radians(float(lat2))
    lon2_rad = math.radians(float(lon2))

    diff_lat = lat2_rad - lat1_rad
    diff_lon = lon2_rad - lon1_rad

    a = (
        math.sin(diff_lat / 2) ** 2
        + math.cos(lat1_rad)
        * math.cos(lat2_rad)
        * math.sin(diff_lon / 2) ** 2
    )

    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return round(earth_radius_m * c)


def enrich_stop(stop, lat=None, lon=None):
    services = get_services(stop["id"])

    enriched = {
        "id": stop["id"],
        "name": stop["name"],
        "lat": stop["lat"],
        "lon": stop["lon"],
        "services": services,
        "modes": guess_modes_from_services(services),
        "hub": is_hub(stop["name"]),
    }

    if lat is not None and lon is not None:
        enriched["distance_m"] = calculate_distance_m(
            lat,
            lon,
            stop["lat"],
            stop["lon"],
        )

    return enriched


def merge_services(existing_services, new_services):
    for mode, lines in new_services.items():
        existing_services.setdefault(mode, [])

        for line in lines:
            if line not in existing_services[mode]:
                existing_services[mode].append(line)

    for mode in existing_services:
        existing_services[mode].sort()

    return existing_services


def merge_stops_by_name(results):
    grouped = {}

    for stop in results:
        name = stop["name"]

        if name not in grouped:
            grouped[name] = {
                "id": stop["id"],
                "name": stop["name"],
                "lat": stop["lat"],
                "lon": stop["lon"],
                "distance_m": stop.get("distance_m"),
                "services": stop.get("services", {}),
                "modes": list(stop.get("modes", [])),
                "hub": stop.get("hub", False),
            }
            continue

        existing = grouped[name]

        if (
            stop.get("distance_m") is not None
            and (
                existing.get("distance_m") is None
                or stop["distance_m"] < existing["distance_m"]
            )
        ):
            existing["distance_m"] = stop["distance_m"]
            existing["lat"] = stop["lat"]
            existing["lon"] = stop["lon"]
            existing["id"] = stop["id"]

        existing["services"] = merge_services(
            existing.get("services", {}),
            stop.get("services", {}),
        )

        existing["modes"] = guess_modes_from_services(existing["services"])
        existing["hub"] = existing.get("hub", False) or stop.get("hub", False)

    return list(grouped.values())


def load_stops():
    global cached_stops

    if cached_stops is not None:
        return cached_stops

    stops = []

    with zipfile.ZipFile("data/PID_GTFS.zip", "r") as zip_file:
        with zip_file.open("stops.txt") as stops_file:
            reader = csv.DictReader(
                (line.decode("utf-8") for line in stops_file)
            )

            for row in reader:
                stops.append(
                    {
                        "id": row["stop_id"],
                        "name": row["stop_name"],
                        "lat": row["stop_lat"],
                        "lon": row["stop_lon"],
                    }
                )

    cached_stops = stops
    return cached_stops


def search_stops(query: str, lat=None, lon=None):
    results = []

    for stop in load_stops():
        if query.lower() in stop["name"].lower():
            results.append(enrich_stop(stop, lat, lon))

    merged = merge_stops_by_name(results)

    if lat is not None and lon is not None:
        merged.sort(key=lambda item: item.get("distance_m", 999999))

    return merged[:20]


def get_stop_by_id(stop_id: str):
    for stop in load_stops():
        if stop["id"] == stop_id:
            return enrich_stop(stop)

    return {"error": "Stop not found"}


def find_nearest_stops(lat: float, lon: float):
    results = []

    for stop in load_stops():
        results.append(enrich_stop(stop, lat, lon))

    merged = merge_stops_by_name(results)
    merged.sort(key=lambda item: item.get("distance_m", 999999))

    return merged[:10]


@router.get("/test-czech")
def test_czech():
    return JSONResponse(
        content={"message": "Příliš žluťoučký kůň úpěl ďábelské ódy"},
        media_type="application/json; charset=utf-8",
    )


@router.get("/stops")
def stops():
    return JSONResponse(
        content=load_stops(),
        media_type="application/json; charset=utf-8",
    )


@router.get("/search-stop")
def search_stop(
    query: str,
    lat: Optional[float] = None,
    lon: Optional[float] = None,
):
    return JSONResponse(
        content=search_stops(query, lat, lon),
        media_type="application/json; charset=utf-8",
    )


@router.get("/stop")
def stop(stop_id: str):
    return JSONResponse(
        content=get_stop_by_id(stop_id),
        media_type="application/json; charset=utf-8",
    )


@router.get("/nearest")
def nearest(lat: float, lon: float):
    return JSONResponse(
        content=find_nearest_stops(lat, lon),
        media_type="application/json; charset=utf-8",
    )