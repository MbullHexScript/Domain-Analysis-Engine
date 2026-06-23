import requests
from bs4 import BeautifulSoup


def extract_html_features(url):

    try:

        response = requests.get(
            url,
            timeout=10,
            headers={"User-Agent": "Mozilla/5.0"},
        )

        soup = BeautifulSoup(
            response.text,
            "html.parser",
        )

        features = {}

        # Redirect
        features["NoOfURLRedirect"] = len(response.history)

        features["NoOfSelfRedirect"] = 0

        for redirect in response.history:
            if redirect.url == response.url:
                features["NoOfSelfRedirect"] += 1

        # Basic HTML Features
        features["HasTitle"] = int(soup.title is not None)

        description = soup.find(
            "meta",
            attrs={"name": "description"},
        )

        features["HasDescription"] = int(description is not None)

        favicon = soup.find(
            "link",
            rel=lambda x: x and "icon" in x.lower(),
        )

        features["HasFavicon"] = int(favicon is not None)

        features["NoOfImage"] = len(soup.find_all("img"))

        features["NoOfCSS"] = len(soup.find_all("link", rel="stylesheet"))

        features["NoOfJS"] = len(soup.find_all("script"))

        features["NoOfiFrame"] = len(soup.find_all("iframe"))

        # Source Code Features
        lines = response.text.splitlines()

        features["LineOfCode"] = len(lines)

        features["LargestLineLength"] = max(
            [len(line) for line in lines],
            default=0,
        )

        # Robots
        robots_meta = soup.find(
            "meta",
            attrs={"name": "robots"},
        )

        features["Robots"] = int(robots_meta is not None)

        # Responsive
        viewport = soup.find(
            "meta",
            attrs={"name": "viewport"},
        )

        features["IsResponsive"] = int(viewport is not None)

        # Form Features
        features["HasSubmitButton"] = int(
            len(soup.find_all("input", {"type": "submit"})) > 0
        )

        features["HasHiddenFields"] = int(
            len(soup.find_all("input", {"type": "hidden"})) > 0
        )

        features["HasPasswordField"] = int(
            len(soup.find_all("input", {"type": "password"})) > 0
        )

        forms = soup.find_all("form")

        features["HasExternalFormSubmit"] = 0

        for form in forms:
            action = form.get("action", "")
            if action.startswith("http"):
                features["HasExternalFormSubmit"] = 1
                break

        html_text = response.text.lower()

        # Social Network
        social_keywords = [
            "facebook",
            "instagram",
            "twitter",
            "linkedin",
            "youtube",
            "tiktok",
        ]

        features["HasSocialNet"] = int(
            any(keyword in html_text for keyword in social_keywords)
        )

        # Popup Detection
        popup_keywords = ["window.open", "popup", "modal"]

        features["NoOfPopup"] = sum(
            html_text.count(keyword) for keyword in popup_keywords
        )

        # Bank Detection
        bank_keywords = [
            "bank",
            "banking",
            "bca",
            "bni",
            "bri",
            "mandiri",
            "cimb",
            "permata",
        ]

        features["Bank"] = 0

        # Payment Detection
        pay_keywords = [
            "payment",
            "pay",
            "paypal",
            "checkout",
            "transaction",
            "invoice",
        ]

        features["Pay"] = 0

        # Crypto Detection
        crypto_keywords = [
            "crypto",
            "bitcoin",
            "ethereum",
            "usdt",
            "wallet",
            "blockchain",
        ]

        features["Crypto"] = 0

        # Copyright
        features["HasCopyrightInfo"] = int("copyright" in html_text or "©" in html_text)

        # Reference Analysis
        all_links = soup.find_all("a")

        external_ref = 0
        self_ref = 0
        empty_ref = 0

        domain = response.url.split("/")[2]

        for link in all_links:

            href = link.get("href")

            if not href:
                empty_ref += 1
                continue

            href = href.strip()

            if href == "" or href == "#":
                empty_ref += 1
            elif domain in href:
                self_ref += 1
            elif href.startswith("http"):
                external_ref += 1

        features["NoOfExternalRef"] = external_ref
        features["NoOfSelfRef"] = self_ref
        features["NoOfEmptyRef"] = empty_ref

        return features

    except Exception as e:

        print("Error:", e)

        return {}


if __name__ == "__main__":

    url = "https://www.google.com"

    result = extract_html_features(url)

    for key, value in result.items():
        print(f"{key}: {value}")

    print("\nJumlah fitur:", len(result))
