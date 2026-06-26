from fastapi import APIRouter
from fastapi.responses import JSONResponse
from engine.route_engine import get_route

router = APIRouter()


@router.get("/route")
def route(from_stop: str, to_stop: str):
    return JSONResponse(
        content=get_route(from_stop, to_stop),
        media_type="application/json; charset=utf-8"
    )