from flask import Blueprint, request, jsonify
from app.services.url_model import predict_url

url_bp = Blueprint("url_bp", __name__)

@url_bp.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()
    url = data.get("url", "").strip()

    if not url:
        return jsonify({"error": "URL is required"}), 400

    if not url.startswith(("http://", "https://")):
        return jsonify({"error": "Invalid URL format"}), 400

    result = predict_url(url)
    return jsonify(result)
