from urllib.parse import urlparse

url = "https://www.google.com"

parsed = urlparse(url)

print("URL:", url)
print("Domain:", parsed.netloc)
