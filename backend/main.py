from fastapi import FastAPI

app = FastAPI()


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
        "recommended_route": "Metro A",
        "risk": "low"
    }