from fastapi.responses import JSONResponse

from fastapi import APIRouter
import zipfile
import csv

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
                        "name": row["stop_name"]
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