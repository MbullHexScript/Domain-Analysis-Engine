import sys
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

sys.path.append(BASE_DIR)
from app.features.feature_extractor import extract_features

url = "https://www.google.com"

features = extract_features(url)

print(features)
print()
print("Jumlah fitur:", len(features))
