from fastapi import APIRouter

router = APIRouter()

@router.get("/route")
def get_route(from_stop: str, to_stop: str):
    return {

        "from": from_stop,
        "to": to_stop,
        "recommended_route": "Metro A + Bus 59",
        "risk": "low",
        "reliability": 95
    }