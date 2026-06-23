import pandas as pd
import requests
import json
from tabulate import tabulate

# ── Config ──────────────────────────────────────────────────────────────────
FLASK_URL = "http://127.0.0.1:5000/predict"
DATASET_PATH = "../dataset/PhiUSIIL_Phishing_URL_Dataset.csv"
SAMPLE_PER_CLASS = 10
# ────────────────────────────────────────────────────────────────────────────


def test_url(url: str) -> dict:
    try:
        res = requests.post(
            FLASK_URL,
            json={"url": url},
            timeout=60,
        )
        data = res.json()
        return {
            "prediction": data.get("label", "Error"),
            "confidence": (
                data["confidence"]["legitimate"]
                if data.get("prediction") == 1
                else data["confidence"]["phishing"]
            ),
            "error": None,
        }
    except Exception as e:
        return {"prediction": "Error", "confidence": 0, "error": str(e)}


def main():
    print("Loading dataset...")
    df = pd.read_csv(DATASET_PATH)

    phishing_urls = df[df["label"] == 0]["URL"].dropna().head(SAMPLE_PER_CLASS).tolist()
    legit_urls = df[df["label"] == 1]["URL"].dropna().head(SAMPLE_PER_CLASS).tolist()

    samples = [(u, "Phishing") for u in phishing_urls] + [
        (u, "Legitimate") for u in legit_urls
    ]

    print(f"\nTesting {len(samples)} URLs against Flask app...\n")

    rows = []
    correct = 0
    errors = 0

    for i, (url, expected) in enumerate(samples, 1):
        short_url = url[:55] + "..." if len(url) > 55 else url
        print(f"[{i:02d}/{len(samples)}] {short_url}")

        result = test_url(url)

        if result["error"]:
            status = "❌ ERROR"
            errors += 1
        elif result["prediction"] == expected:
            status = "✅ CORRECT"
            correct += 1
        else:
            status = "❌ WRONG"

        rows.append(
            [
                short_url,
                expected,
                result["prediction"],
                f"{result['confidence']:.1f}%",
                status,
            ]
        )

    # ── Summary ─────────────────────────────────────────────────────────────
    total = len(samples)
    tested = total - errors
    accuracy = (correct / tested * 100) if tested > 0 else 0

    print("\n" + "=" * 80)
    print("HASIL VALIDASI REAL-WORLD")
    print("=" * 80)
    print(
        tabulate(
            rows,
            headers=["URL", "Expected", "Prediction", "Confidence", "Status"],
            tablefmt="rounded_outline",
        )
    )

    print(f"""
──────────────────────────────
 Total URL   : {total}
 Tested      : {tested}
 Correct     : {correct}
 Wrong       : {tested - correct}
 Errors      : {errors}
 Accuracy    : {accuracy:.2f}%
──────────────────────────────
""")

    # Per-class breakdown
    phishing_rows = [r for r in rows if r[1] == "Phishing" and "ERROR" not in r[4]]
    legit_rows = [r for r in rows if r[1] == "Legitimate" and "ERROR" not in r[4]]

    p_correct = sum(1 for r in phishing_rows if "CORRECT" in r[4])
    l_correct = sum(1 for r in legit_rows if "CORRECT" in r[4])

    print(
        f"  Phishing   accuracy : {p_correct}/{len(phishing_rows)} = {p_correct/len(phishing_rows)*100:.1f}%"
        if phishing_rows
        else ""
    )
    print(
        f"  Legitimate accuracy : {l_correct}/{len(legit_rows)}  = {l_correct/len(legit_rows)*100:.1f}%"
        if legit_rows
        else ""
    )
    print()


if __name__ == "__main__":
    main()
