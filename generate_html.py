import requests
from bs4 import BeautifulSoup
from datetime import datetime

URL = "https://www.hemmings.com/classifieds/cars-for-sale"

headers = {
    "User-Agent": "Mozilla/5.0"
}

response = requests.get(URL, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")

cars = []

# Hemmings listing cards (as of May 2025)
cards = soup.select("ul.listings > li.listing")

for card in cards[:10]:
    try:
        title = card.select_one("div.listing-title").get_text(strip=True)
        price = card.select_one("div.listing-price").get_text(strip=True)
        location = card.select_one("div.listing-location").get_text(strip=True)
        link = "https://www.hemmings.com" + card.select_one("a")["href"]
        image = card.select_one("img")["src"]

        cars.append({
            "title": title,
            "price": price,
            "location": location,
            "image": image,
            "link": link
        })
    except Exception:
        continue

# Generate HTML
today = datetime.now().strftime("%Y-%m-%d")
html = f"""<!DOCTYPE html>
<html>
<head>
  <title>Classic Car Listings - {today}</title>
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <style>
    body {{ font-family: sans-serif; padding: 2rem; background: #f4f4f4; }}
    .car {{ background: white; margin: 1rem 0; padding: 1rem; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
    img {{ max-width: 100%; border-radius: 6px; }}
    h2 {{ margin: 0.5rem 0; }}
  </style>
</head>
<body>
  <h1>Top Classic Cars for Sale – {today}</h1>
"""

for car in cars:
    html += f"""
    <div class="car">
      <img src="{car['image']}" alt="{car['title']}">
      <h2>{car['title']}</h2>
      <p><strong>Price:</strong> {car['price']}<br>
      <strong>Location:</strong> {car['location']}<br>
      <a href="{car['link']}" target="_blank">View listing</a></p>
    </div>
    """

html += "</body></html>"

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)
