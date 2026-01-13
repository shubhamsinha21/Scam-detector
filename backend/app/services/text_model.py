import joblib
import os

BASE_DIR = os.path.dirname(__file__)
MODEL_DIR = os.path.abspath(os.path.join(BASE_DIR, "../models"))

model = joblib.load(os.path.join(MODEL_DIR, "text_scam_model.joblib"))
vectorizer = joblib.load(os.path.join(MODEL_DIR, "tfidf_vectorizer.joblib"))

def predict_text(text: str):
    x = vectorizer.transform([text])
    pred = model.predict(x)[0]
    proba = model.predict_proba(x)[0][pred]
    return {
        "prediction": "scam" if pred == 1 else "legitimate",
        "confidence": round(float(proba), 2)
    }