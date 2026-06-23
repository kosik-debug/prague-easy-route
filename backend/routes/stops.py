from fastapi.responses import JSONResponse

from fastapi import APIRouter
import zipfile
import csv
import math

router = APIRouter()
cached_stops = None


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
        "lon": row["stop_lon"]
    }
                )

                if len(stops) >= 2000:
                    break

    cached_stops = stops
    return cached_stops


def search_stops(query: str):
    results = []
    for stop in load_stops():
        if query.lower() in stop["name"].lower():
            results.append(stop)
    return results[:10]

def get_stop_by_id(stop_id: str):
    for stop in load_stops():
        if stop["id"] == stop_id:
            return stop
    return {"error": "Stop not found"}

@router.get("/test-czech")
def test_czech():
    return JSONResponse(
        content={
            "message": "Příliš žluťoučký kůň úpěl ďábelské ódy"
        },
        media_type="application/json; charset=utf-8"
    )

@router.get("/stops")
def stops():
    return JSONResponse(
        content=load_stops(),
        media_type="application/json; charset=utf-8"
    )
@router.get("/search-stop")
def search_stop(query: str):
    return JSONResponse(
        content=search_stops(query),
        media_type="application/json; charset=utf-8"
    )
@router.get("/stop")
def stop(stop_id: str):

    return JSONResponse(
        content=get_stop_by_id(stop_id),
        media_type="application/json; charset=utf-8"
    )
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

def find_nearest_stops(lat: float, lon: float):
    results = []

    for stop in load_stops():
        distance = calculate_distance_m(
            lat,
            lon,
            stop["lat"],
            stop["lon"]
        )

        results.append(
            {
                "id": stop["id"],
                "name": stop["name"],
                "lat": stop["lat"],
                "lon": stop["lon"],
                "distance_m": distance
            }
        )

    results.sort(key=lambda item: item["distance_m"])

    return results[:5]

@router.get("/nearest")
def nearest(lat: float, lon: float):
    return JSONResponse(
        content=find_nearest_stops(lat, lon),
        media_type="application/json; charset=utf-8"
    )
