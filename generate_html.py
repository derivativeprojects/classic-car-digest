from datetime import datetime
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

URL = "https://www.hemmings.com/classifieds/cars-for-sale?sort=latest"

def get_listings():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(URL, timeout=60000)
        page.wait_for_timeout(8000)  # wait for JS-rendered listings to load
        html = page.content()
        browser.close()
        return html

html = get_listings()
soup = BeautifulSoup(html, "html.parser")

cars = []

for card in soup.select("a[href^='/classifieds/cars-for-sale/']"):
    try:
        title = card.get_text(strip=True)
        link = "https://www.hemmings.com" + card["href"]
        image_tag = card.select_one("img")
        image = image_tag["src"] if image_tag and "src" in image_tag.attrs else ""
        price_tag = card.find_next("div", class_="pricing")
        price = price_tag.get_text(strip=True) if price_tag else "Price not listed"

        if title and image:
            cars.append({
                "title": title,
                "price": price,
                "location": "—",
                "image": image,
                "link": link
            })

        if len(cars) >= 10:
            break
    except Exception:
        continue

# Generate the HTML page
today = datetime.now().strftime("%Y-%m-%d")
html_out = f"""<!DOCTYPE html>
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
    html_out += f"""
    <div class="car">
      <img src="{car['image']}" alt="{car['title']}">
      <h2>{car['title']}</h2>
      <p><strong>Price:</strong> {car['price']}<br>
      <strong>Location:</strong> {car['location']}<br>
      <a href="{car['link']}" target="_blank">View listing</a></p>
    </div>
    """

html_out += "</body></html>"

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html_out)
