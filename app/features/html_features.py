import re
from playwright.sync_api import sync_playwright
from urllib.parse import urlparse

# Default fallback jika HTML extraction gagal
_DEFAULT_HTML_FEATURES = {
    "NoOfURLRedirect": 0,
    "NoOfSelfRedirect": 0,
    "HasTitle": 0,
    "HasDescription": 0,
    "HasFavicon": 0,
    "NoOfImage": 0,
    "NoOfCSS": 0,
    "NoOfJS": 0,
    "NoOfiFrame": 0,
    "LineOfCode": 0,
    "LargestLineLength": 0,
    "Robots": 0,
    "IsResponsive": 0,
    "HasSubmitButton": 0,
    "HasHiddenFields": 0,
    "HasPasswordField": 0,
    "HasExternalFormSubmit": 0,
    "HasSocialNet": 0,
    "NoOfPopup": 0,
    "Bank": 0,
    "Pay": 0,
    "Crypto": 0,
    "HasCopyrightInfo": 0,
    "NoOfExternalRef": 0,
    "NoOfSelfRef": 0,
    "NoOfEmptyRef": 0,
}


def _match_keywords(html_lower: str, patterns: list[str]) -> int:
    """Whole-word keyword matching pakai regex."""
    return int(any(re.search(p, html_lower) for p in patterns))


def extract_html_features(url: str) -> dict:
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(
                user_agent=(
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/120.0.0.0 Safari/537.36"
                )
            )
            page = context.new_page()

            # Track redirects
            redirect_urls = []

            def on_response(response):
                if response.status in (301, 302, 303, 307, 308):
                    redirect_urls.append(response.url)

            page.on("response", on_response)

            # Timeout 30s, fallback ke domcontentloaded jika networkidle gagal
            try:
                page.goto(url, wait_until="networkidle", timeout=30000)
            except Exception:
                page.goto(url, wait_until="domcontentloaded", timeout=30000)

            final_url = page.url
            parsed_final = urlparse(final_url)
            domain = parsed_final.netloc

            features = {}

            # Redirects
            features["NoOfURLRedirect"] = len(redirect_urls)
            features["NoOfSelfRedirect"] = sum(
                1 for r in redirect_urls if urlparse(r).netloc == domain
            )

            # Rendered HTML
            html_text = page.content()
            html_lower = html_text.lower()

            # Title
            title = page.title()
            features["HasTitle"] = int(bool(title and title.strip()))

            # Description
            features["HasDescription"] = int(
                page.query_selector('meta[name="description"]') is not None
            )

            # Favicon
            features["HasFavicon"] = int(
                page.query_selector('link[rel*="icon"], link[rel*="shortcut"]')
                is not None
            )

            # Assets
            features["NoOfImage"] = len(page.query_selector_all("img"))
            features["NoOfCSS"] = len(page.query_selector_all('link[rel="stylesheet"]'))
            features["NoOfJS"] = len(page.query_selector_all("script"))
            features["NoOfiFrame"] = len(page.query_selector_all("iframe"))

            # Source code metrics
            lines = html_text.splitlines()
            features["LineOfCode"] = len(lines)
            features["LargestLineLength"] = max((len(l) for l in lines), default=0)

            # Robots & Responsive
            features["Robots"] = int(
                page.query_selector('meta[name="robots"]') is not None
            )
            features["IsResponsive"] = int(
                page.query_selector('meta[name="viewport"]') is not None
            )

            # Form features
            features["HasSubmitButton"] = int(
                len(
                    page.query_selector_all(
                        'input[type="submit"], button[type="submit"]'
                    )
                )
                > 0
            )
            features["HasHiddenFields"] = int(
                len(page.query_selector_all('input[type="hidden"]')) > 0
            )
            features["HasPasswordField"] = int(
                len(page.query_selector_all('input[type="password"]')) > 0
            )

            has_external_form = 0
            for form in page.query_selector_all("form"):
                action = form.get_attribute("action") or ""
                if action.startswith("http") and domain not in action:
                    has_external_form = 1
                    break
            features["HasExternalFormSubmit"] = has_external_form

            # Social network (substring ok — nama platform spesifik)
            social_keywords = [
                "facebook",
                "instagram",
                "twitter",
                "linkedin",
                "youtube",
                "tiktok",
            ]
            features["HasSocialNet"] = int(
                any(kw in html_lower for kw in social_keywords)
            )

            # Popup
            popup_keywords = ["window.open", "popup", "modal"]
            features["NoOfPopup"] = sum(html_lower.count(kw) for kw in popup_keywords)

            # Bank — whole-word matching
            features["Bank"] = _match_keywords(
                html_lower,
                [
                    r"\bbank\b",
                    r"\bbanking\b",
                    r"\bbca\b",
                    r"\bbni\b",
                    r"\bbri\b",
                    r"\bmandiri\b",
                    r"\bcimb\b",
                    r"\bpermata\b",
                ],
            )

            # Pay — whole-word matching (hindari "display", "company", dll)
            features["Pay"] = _match_keywords(
                html_lower,
                [
                    r"\bpayment\b",
                    r"\bpaypal\b",
                    r"\bcheckout\b",
                    r"\btransaction\b",
                    r"\binvoice\b",
                ],
            )

            # Crypto — whole-word matching
            features["Crypto"] = _match_keywords(
                html_lower,
                [
                    r"\bcrypto\b",
                    r"\bcryptocurrency\b",
                    r"\bbitcoin\b",
                    r"\bethereum\b",
                    r"\busdt\b",
                    r"\bblockchain\b",
                    r"\bnft\b",
                    r"\bweb3\b",
                ],
            )

            # Copyright
            features["HasCopyrightInfo"] = int(
                "copyright" in html_lower or "©" in html_text
            )

            # Reference analysis
            external_ref = self_ref = empty_ref = 0
            for link in page.query_selector_all("a"):
                href = link.get_attribute("href")
                if not href:
                    empty_ref += 1
                    continue
                href = href.strip()
                if href in ("", "#"):
                    empty_ref += 1
                elif href.startswith("http"):
                    if domain in href:
                        self_ref += 1
                    else:
                        external_ref += 1
                else:
                    # relative path → self ref
                    self_ref += 1

            features["NoOfExternalRef"] = external_ref
            features["NoOfSelfRef"] = self_ref
            features["NoOfEmptyRef"] = empty_ref

            browser.close()
            return features

    except Exception as e:
        print(f"[html_features] Error ({url}): {e}")
        print("[html_features] Returning default fallback values.")
        return dict(_DEFAULT_HTML_FEATURES)


if __name__ == "__main__":
    url = "https://www.google.com"
    result = extract_html_features(url)
    for key, value in result.items():
        print(f"{key}: {value}")
    print("\nJumlah fitur:", len(result))
