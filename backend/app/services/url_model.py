import re
import joblib
import os
import numpy as np

# -------------- Model loader ----------------

MODEL_PATH = os.path.join(os.path.dirname(__file__), "../models/url_phishing_model.joblib")
model = joblib.load(MODEL_PATH)

# -------------- Feature Extraction ----------------
def extract_features(url: str) -> np.array:
    features = {}
    features["url_length"] = len(url)
    features["dot_count"] = url.count(".")
    features["hyphen_count"] = url.count("-")
    features["special_char_count"] = len(re.findall(r"[@?=&]", url))
    features["has_ip"] = 1 if re.search(r"\d+\.\d+\.\d+\.\d+", url) else 0
    features["https"] = 1 if url.startswith("https") else 0
    features["suspicious_words"] = 1 if any(word in url.lower() for word in ["login", "secure", "verify", "update"]) else 0
    return np.array(list(features.values())).reshape(1, -1)

# -------------- Prediction function ----------------
def predict_url(url:str):
    features = extract_features(url)
    prediction = model.predict(features)[0] # 0 or 1
    confidence = model.predict_proba(features)[0][prediction] # probability of predicted class
    result = {
        "prediction": "phishing" if prediction == 1 else "safe",
        "confidence": round(float(confidence), 2)
    }
    return result
 