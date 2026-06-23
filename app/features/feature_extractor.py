from features.url_features import extract_url_features
from features.html_features import extract_html_features


def extract_features(url):

    features = {}

    features.update(extract_url_features(url))

    features.update(extract_html_features(url))

    return features


if __name__ == "__main__":

    url = "https://www.google.com"

    result = extract_features(url)

    print(result)

    print("\nTotal Features:", len(result))
