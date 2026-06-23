from fastapi import APIRouter

router = APIRouter()


@router.get("/stops")
def stops():
    return [
        {
            "name": "Hlavni nadrazi",
            "type": "metro/tram/train"
        },
        {
            "name": "Muzeum",
            "type": "metro"
        },
        {
            "name": "Andel",
            "type": "metro/tram/bus"
        },
        {
            "name": "Letiste",
            "type": "bus/airport"
        }
    ]