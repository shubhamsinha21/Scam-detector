# type: ignore
import warnings
warnings.filterwarnings("ignore", category=RuntimeWarning)

import pandas as pd 
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
import joblib
import os
import logging

# ------------------ Logging Setup ------------------
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# ----------------- Load Dataset --------------------

logging.info("Loading email dataset...")
df = pd.read_csv("data/emails.csv")

texts = df["text"].astype(str).tolist()
labels = df["label_num"].astype(int).tolist()
logging.info(f"Dataset loaded with {len(texts)} records.")

# ----------------- Split --------------------

logging.info("Splitting dataset into train & test...")
x_train, x_test, y_train, y_test = train_test_split(
    texts, labels,
    test_size=0.2,
    random_state=42,
    stratify=labels
)
logging.info(f"Train size: {len(x_train)}, Test size: {len(x_test)}")

# ----------------- TF-IDF --------------------

logging.info("Vectorizing text using TF-IDF...")
vectorizer = TfidfVectorizer(
    max_features = 5000,
    stop_words = "english"
)

x_train_vec = vectorizer.fit_transform(x_train)
x_test_vec = vectorizer.transform(x_test)
logging.info("TF-IDF vectorization completed.")

# ----------------- Model --------------------

logging.info("Training Logistic Regression model...")
model = LogisticRegression(max_iter=1000)
model.fit(x_train_vec, y_train)
logging.info("Model training completed.")

# ----------------- Evaluation --------------------

logging.info("Evaluating model...")
y_pred = model.predict(x_test_vec)
logging.info("\n" + classification_report(y_test, y_pred))

# ----------------- Save model & vectorizer --------------------

os.makedirs("../../backend/app/models/", exist_ok=True)

joblib.dump(model, "../../backend/app/models/text_scam_model.joblib")
joblib.dump(vectorizer, "../../backend/app/models/tfidf_vectorizer.joblib")

logging.info("Model & Vectorizer saved successfully.")