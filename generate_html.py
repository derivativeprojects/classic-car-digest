import requests
from bs4 import BeautifulSoup
from datetime import datetime

URL = "https://classiccars.com/listings/find/all-years/all-makes/all-models?sort=recently-listed"
headers = {"User-Agent": "Mozilla/5.0"}

response = requests.get(URL, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")

cars = []
listings = soup.select("div.vehicle-card")

for listing in listings:
    try:
        title = listing.select_one("h2.vehicle-title").get_text(strip=True)
        price = listing.select_one("span.price").get_text(strip=True)
        location = listing.select_one("div.vehicle-location").get_text(strip=True)
        image = listing.select_one("img")["src"]
        link = "https://classiccars.com" + listing.select_one("a.vehicle-card-link")["href"]

        cars.append({
            "title": title,
            "price": price,
            "location": location,
            "image": image,
            "link": link
        })

        if len(cars) == 10:
            break
    except Exception:
        continue

# Generate HTML
today = datetime.now().strftime("%Y-%m-%d")
html = f"""<!DOCTYPE html>
<html><head>
  <title>Classic Car Listings - {today}</title>
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <style>
    body {{ font-family: sans-serif; padding: 2rem; background: #f4f4f4; }}
    .car {{ background: white; margin: 1rem 0; padding: 1rem; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
    img {{ max-width: 100%; border-radius: 6px; }}
    h2 {{ margin: 0.5rem 0; }}
  </style>
</head><body>
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
