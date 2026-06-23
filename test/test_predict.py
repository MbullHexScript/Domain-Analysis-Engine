import sys
import os
import joblib
import pandas as pd

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

sys.path.append(BASE_DIR)

from app.features.feature_extractor import extract_features

# Load Model
model = joblib.load(os.path.join(BASE_DIR, "models", "phishing_model_44.pkl"))

feature_names = joblib.load(os.path.join(BASE_DIR, "models", "feature_names_44.pkl"))

# Test URL
url = "https://www.google.com/"

features = extract_features(url)

print("Jumlah feature_names:", len(feature_names))
print("Jumlah features:", len(features))

missing = [col for col in feature_names if col not in features]

extra = [col for col in features if col not in feature_names]

print("Missing:", missing)
print("Extra:", extra)

for k, v in features.items():
    print(k, ":", v)

# Susun urutan fitur sesuai model
input_data = pd.DataFrame(
    [[features[col] for col in feature_names]], columns=feature_names
)

prediction = model.predict(input_data)[0]

probability = model.predict_proba(input_data)[0]

print("Prediction :", prediction)
print("Probability:", probability)
