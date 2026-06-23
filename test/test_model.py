import os
import joblib

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

model_path = os.path.join(BASE_DIR, "models", "phishing_model_44.pkl")

feature_path = os.path.join(BASE_DIR, "models", "feature_names_44.pkl")

model = joblib.load(model_path)
features = joblib.load(feature_path)

print(type(model))
print("Jumlah fitur:", len(features))
