from fastapi import APIRouter
from routes.stops import load_stops

router = APIRouter()


@router.get("/route")
def get_route(from_stop: str, to_stop: str):

    stops = load_stops()

    from_exists = any(
        from_stop.lower() in stop["name"].lower()
        for stop in stops
    )

    to_exists = any(
        to_stop.lower() in stop["name"].lower()
        for stop in stops
    )

    if not from_exists:
        return {
            "error": f"Start stop '{from_stop}' not found"
        }

    if not to_exists:
        return {
            "error": f"Destination stop '{to_stop}' not found"
        }

    return {
        "from": from_stop,
        "to": to_stop,
        "recommended_route": "PID route placeholder",
        "risk": "low",
        "reliability": 95
    }