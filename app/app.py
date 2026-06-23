from flask import Flask, render_template, request, jsonify
import pickle
import numpy as np
import os
import sys

# Path setup
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)

from features.feature_extractor import extract_features

app = Flask(__name__)

# Load model & feature names
MODEL_PATH = os.path.join(BASE_DIR, "..", "models", "phishing_model_44.pkl")
FEATURES_PATH = os.path.join(BASE_DIR, "..", "models", "feature_names_44.pkl")

with open(MODEL_PATH, "rb") as f:
    model = pickle.load(f)

with open(FEATURES_PATH, "rb") as f:
    feature_names = pickle.load(f)


def predict_url(url: str):
    """Extract features and return prediction + confidence."""
    raw_features = extract_features(url)

    # Build feature vector in correct order
    feature_vector = []
    missing = []

    for name in feature_names:
        if name in raw_features:
            feature_vector.append(raw_features[name])
        else:
            feature_vector.append(0)
            missing.append(name)

    if missing:
        print(f"Warning: Missing features filled with 0 → {missing}")

    X = np.array(feature_vector).reshape(1, -1)
    prediction = model.predict(X)[0]
    proba = model.predict_proba(X)[0]

    return {
        "url": url,
        "prediction": int(prediction),
        "label": "Legitimate" if prediction == 1 else "Phishing",
        "confidence": {
            "phishing": round(float(proba[0]) * 100, 2),
            "legitimate": round(float(proba[1]) * 100, 2),
        },
        "features": raw_features,
    }


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()
    url = data.get("url", "").strip()

    if not url:
        return jsonify({"error": "URL tidak boleh kosong"}), 400

    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    try:
        result = predict_url(url)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/health")
def health():
    return jsonify({"status": "ok", "features_loaded": len(feature_names)})


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
