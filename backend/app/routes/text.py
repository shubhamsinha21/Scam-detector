from flask import Blueprint, request, jsonify
from app.services.text_model import predict_text
import PyPDF2

text_bp = Blueprint("text_bp", __name__)

@text_bp.route("/scam", methods=["POST"])
def detect_scam():
    file = request.files.get("file")
    if not file:
        return jsonify({"error": "File required"}), 400
    
    ext = file.filename.split(".")[-1].lower()
    if ext not in ["txt", "pdf"]:
        return jsonify({"error": "Only PDF/TXT supported"}), 400
    
    # Extract text
    if ext == "txt":
        text = file.read().decode("utf-8")
    else:
        pdf_reader = PyPDF2.PdfReader(file)
        pages = [p.extract_text() for p in pdf_reader.pages if p.extract_text()]
        text = " ".join(pages)

        
    # Predict
    result = predict_text(text)
    return jsonify(result)