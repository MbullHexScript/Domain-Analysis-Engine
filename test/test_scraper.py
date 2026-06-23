import requests
from bs4 import BeautifulSoup

url = "https://www.google.com"

response = requests.get(
    url,
    timeout=10,
    headers={
        "User-Agent": "Mozilla/5.0"
    }
)

print("Status Code:", response.status_code)

soup = BeautifulSoup(response.text, "html.parser")

title = soup.title.string if soup.title else "No Title"

print("Title:", title)

print("Jumlah Link:", len(soup.find_all("a")))
print("Jumlah Form:", len(soup.find_all("form")))
print("Jumlah Gambar:", len(soup.find_all("img")))
print("Jumlah Script:", len(soup.find_all("script")))

print("\n=== Dataset Features ===")

print("HasTitle:", int(soup.title is not None))

description = soup.find(
    "meta",
    attrs={"name": "description"}
)

print("HasDescription:", int(description is not None))

favicon = soup.find(
    "link",
    rel=lambda x: x and "icon" in x.lower()
)

print("HasFavicon:", int(favicon is not None))

print("NoOfImage:", len(soup.find_all("img")))

print("NoOfJS:", len(soup.find_all("script")))

print("NoOfiFrame:", len(soup.find_all("iframe")))
