import requests
from bs4 import BeautifulSoup
from datetime import datetime

URL = "https://www.hemmings.com/classifieds/cars-for-sale?sort=latest"

headers = {
    "User-Agent": "Mozilla/5.0"
}

response = requests.get(URL, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")

# Save for debugging
with open("hemmings_raw.html", "w", encoding="utf-8") as f:
    f.write(soup.prettify())

cars = []

# Each car listing is inside an <article> tag with a link and image
for article in soup.select("article"):
    try:
        link_tag = article.select_one("a[href*='/classifieds/cars-for-sale/']")
        if not link_tag:
            continue

        link = "https://www.hemmings.com" + link_tag["href"]
        title = link_tag.get_text(strip=True)

        image_tag = article.select_one("img")
        image = image_tag["src"] if image_tag and "src" in image_tag.attrs else ""

        price_tag = article.select_one("div.pricing, .listing-price")
        price = price_tag.get_text(strip=True) if price_tag else "Price not listed"

        cars.append({
            "title": title,
            "price": price,
            "location": "—",  # Hemmings doesn't consistently display location in search
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
