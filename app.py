from flask import Flask, request, jsonify, render_template
import requests, os
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

# API Keys from .env file
HERE_API_KEY = os.getenv("HERE_API_KEY")
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")

def geocode_place(place):
    """Converts city names to latitude and longitude coordinates."""
    url = "https://geocode.search.hereapi.com/v1/geocode"
    params = {"q": place, "apiKey": HERE_API_KEY}
    try:
        data = requests.get(url, params=params).json()
        p = data["items"][0]["position"]
        return p["lat"], p["lng"]
    except:
        return None, None

def get_weather(lat, lon):
    """Fetches real-time weather details for the given coordinates."""
    try:
        url = "https://api.openweathermap.org/data/2.5/weather"
        params = {"lat": lat, "lon": lon, "appid": WEATHER_API_KEY, "units": "metric"}
        data = requests.get(url, params=params, timeout=5).json()
        return f"{data['main']['temp']}°C, {data['weather'][0]['description'].title()}"
    except:
        return "Weather unavailable"

@app.route("/")
def home():
    return render_template("index.html", here_api_key=HERE_API_KEY)

@app.route("/route")
def route():
    origin = request.args.get("origin")
    destination = request.args.get("destination")
    
    if not origin or not destination:
        return jsonify({"error": "Missing input"}), 400

    o_lat, o_lng = geocode_place(origin)
    d_lat, d_lng = geocode_place(destination)

    if not o_lat or not d_lat:
        return jsonify({"error": "Invalid city"}), 400

    # Fetch road data with real-time traffic
    r = requests.get(
        "https://router.hereapi.com/v8/routes",
        params={
            "transportMode": "car",
            "origin": f"{o_lat},{o_lng}",
            "destination": f"{d_lat},{d_lng}",
            "return": "summary,polyline",
            "traffic": "enabled",
            "apiKey": HERE_API_KEY
        }
    ).json()

    section = r["routes"][0]["sections"][0]
    return jsonify({
        "distance": round(section["summary"]["length"] / 1000, 2),
        "road_time": section["summary"]["duration"] / 60,
        "polyline": section["polyline"],
        "origin_weather": get_weather(o_lat, o_lng),
        "dest_weather": get_weather(d_lat, d_lng),
        "o_lat": o_lat, "o_lng": o_lng,
        "d_lat": d_lat, "d_lng": d_lng
    })

if __name__ == "__main__":
    app.run(debug=True)