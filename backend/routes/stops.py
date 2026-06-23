from fastapi.responses import JSONResponse

from fastapi import APIRouter
import zipfile
import csv

router = APIRouter()


def load_stops():
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

                if len(stops) >= 20:
                    break

    return stops


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