from flask import Blueprint, request, jsonify
from services.here_service import get_route

commute_bp = Blueprint("commute", __name__)

@commute_bp.route("/commute", methods=["GET"])
def commute():
    origin = request.args.get("origin")
    destination = request.args.get("destination")

    if not origin or not destination:
        return jsonify({"error": "origin and destination required"}), 400

    try:
        route_data = get_route(origin, destination)
        return jsonify(route_data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
