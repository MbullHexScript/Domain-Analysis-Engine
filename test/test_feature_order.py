# test/test_feature_order.py

import os
import joblib

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

feature_names = joblib.load(os.path.join(BASE_DIR, "models", "feature_names_44.pkl"))

for i, feature in enumerate(feature_names):
    print(i + 1, feature)
