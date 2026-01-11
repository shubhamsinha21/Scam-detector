# type: ignore
 
import pandas as pd
import re
from urllib.parse import urlparse
from sklearn.model_selection import train_test_split
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
import joblib
import logging

# ------------------ Logging Setup ------------------
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

'''
--------------- Feature Extraction --------------- 
'''

def extract_features(url):
    features = {}
    features["url_length"] = len(url)
    features["dot_count"] = url.count(".")
    features["hyphen_count"] = url.count("-")
    features["special_char_count"] = len(re.findall(r"[@?=&]", url))
    features["has_ip"] = 1 if re.search(r"\d+\.\d+\.\d+\.\d+", url) else 0
    features["https"] = 1 if url.startswith("https") else 0
    features["suspicious_words"] = 1 if any(word in url.lower() for word in ["login", "secure", "verify", "update"]) else 0
    return features

''' 
 --------------- Load Dataset --------------- 
'''

logging.info("Loading dataset...")
df = pd.read_csv("data/phishing_urls.csv")


''' 
--------------- Keep only phishing & benign --------------- 
'''

df = df[df["type"].isin(["phishing", "benign"])]

'''
--------------- Mapping to binary label --------------- 
'''

df["label"] = df["type"].map({
    "phishing": 1,
    "benign": 0
})

df = df.drop(columns=["type"]) # removing old column
logging.info(f"Dataset loaded with {len(df)} rows.")

'''
--------------- Feature Matrix --------------- 
'''

logging.info("Extracting features from URLs...")
x = pd.DataFrame(df["url"].apply(extract_features).tolist())
y = df["label"]
logging.info("Feature extraction completed.")

'''
--------------- Train/Test split --------------- 
'''

x_train, x_test, y_train, y_test = train_test_split(
    x, y, test_size=0.2, random_state=42
)
logging.info(f"Split dataset: {len(x_train)} training rows, {len(x_test)} test rows.")

'''
--------------- Model training --------------- 
'''

logging.info("Training RandomForest model started...")
model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)
model.fit(x_train, y_train)
logging.info("Training completed.")

'''
--------------- Evaluation --------------- 
'''

logging.info("Evaluating model...")
y_pred = model.predict(x_test)
logging.info("\n" + classification_report(y_test, y_pred))

'''
--------------- Save model --------------- 
'''

joblib.dump(model, "url_phishing_model.joblib")
logging.info("Model saved as url_phishing_model.joblib")