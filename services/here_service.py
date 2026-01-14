import os
import requests

HERE_BASE_URL = "https://router.hereapi.com/v8/routes"

def get_route(origin, destination):
    """
    origin & destination format: "lat,lon"
    Example: "12.9716,77.5946"
    """
    api_key = os.getenv("HERE_API_KEY")

    params = {
        "transportMode": "car",
        "origin": origin,
        "destination": destination,
        "return": "summary",
        "apikey": api_key
    }

    response = requests.get(HERE_BASE_URL, params=params)
    response.raise_for_status()

    data = response.json()

    route = data["routes"][0]["sections"][0]["summary"]

    return {
        "distance_meters": route["length"],
        "duration_seconds": route["duration"]
    }
