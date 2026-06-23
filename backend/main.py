from routes.stops import router as stops_router
from routes.route import router as route_router
from fastapi import FastAPI

app = FastAPI()
app.include_router(stops_router)
app.include_router(route_router)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/")
def home():
    return {
        "app": "Prague Easy Route",
        "version": "0.1"
    }
@app.get("/route")
def route(from_location: str, to_location: str):
    return {
        "from": from_location,
        "to": to_location,
        "recommended_route": "Metro A + Bus 59",
        "risk": "low",
        "reliability_score": 92,
        "reason": "Mene prestupu a nizke riziko zpozdeni"
    }
import requests


@app.get("/external-test")
def external_test():
    response = requests.get("https://api.github.com")
    return response.json()