from urllib.parse import urlparse
import re
import ipaddress


def extract_url_features(url):
    parsed = urlparse(url)

    domain = parsed.netloc

    features = {}

    # URL Features
    features["URLLength"] = len(url)

    features["DomainLength"] = len(domain)

    features["IsHTTPS"] = int(
        parsed.scheme.lower() == "https"
    )

    features["NoOfSubDomain"] = max(
        0,
        len(domain.split(".")) - 2
    )

    features["TLDLength"] = len(
        domain.split(".")[-1]
    )

    # Obfuscation
    features["HasObfuscation"] = int(
        "%" in url
    )

    features["NoOfObfuscatedChar"] = url.count("%")

    if len(url) > 0:
        features["ObfuscationRatio"] = (
            features["NoOfObfuscatedChar"] / len(url)
        )
    else:
        features["ObfuscationRatio"] = 0

    # Character Analysis
    letters = len(
        re.findall(r"[A-Za-z]", url)
    )

    digits = len(
        re.findall(r"\d", url)
    )

    features["NoOfLettersInURL"] = letters

    features["NoOfDegitsInURL"] = digits

    if len(url) > 0:
        features["LetterRatioInURL"] = (
            letters / len(url)
        )

        features["DegitRatioInURL"] = (
            digits / len(url)
        )
    else:
        features["LetterRatioInURL"] = 0
        features["DegitRatioInURL"] = 0

    # Special Characters
    features["NoOfEqualsInURL"] = url.count("=")

    features["NoOfQMarkInURL"] = url.count("?")

    features["NoOfAmpersandInURL"] = url.count("&")

    features["NoOfOtherSpecialCharsInURL"] = len(
        re.findall(r"[@!$*(){}\[\],;]", url)
    )

    total_special = (
        features["NoOfEqualsInURL"]
        + features["NoOfQMarkInURL"]
        + features["NoOfAmpersandInURL"]
        + features["NoOfOtherSpecialCharsInURL"]
    )

    if len(url) > 0:
        features["SpacialCharRatioInURL"] = (
            total_special / len(url)
        )
    else:
        features["SpacialCharRatioInURL"] = 0

    # DomainIP
    try:
        ipaddress.ip_address(domain)
        features["IsDomainIP"] = 1
    except:
        features["IsDomainIP"] = 0

    return features


if __name__ == "__main__":
    test_url = "https://www.google.com/search?q=test"

    result = extract_url_features(test_url)

    print(result)

    print(
        "\nJumlah fitur:",
        len(result)
    )
