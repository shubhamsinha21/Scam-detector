# type: ignore
 
import pandas as pandas
import re
from urllib.parse import urlparse
from sklearn.model_selection import train_test_split


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
 --------------- Load Extraction --------------- 
'''

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

'''
--------------- Feature Matrix --------------- 
'''

x = pd.DataFrame(df["url"].apply(extract_features).tolist())
y = df["label"]

'''
--------------- Train/Test split --------------- 
'''

x_train, x_test, y_train, y_test = train_test_split(
    x, y, test_size=0.2, random_state=42
)

'''
--------------- Model training --------------- 
'''

model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)
model.fit(x_train, y_train)

'''
--------------- Evaluation --------------- 
'''

y_pred = model.predict(x_test)
print("\n Classification Report: \nprint()")
print(classification_report(y_test, y_pred))

'''
--------------- Save model --------------- 
'''

joblib.dump(model, "url_phishing_model.joblib")
print("\n Model saved as url_phishing_model.joblib")
