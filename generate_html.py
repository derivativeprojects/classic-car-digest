from datetime import datetime
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

URL = "https://classiccars.com/listings/find/all-years/all-makes/all-models?sort=recently-listed"

def get_listings():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(URL, timeout=60000)
        page.wait_for_selector("div.vehicle-card", timeout=20000)
        html = page.content()
        browser.close()
        return html

html = get_listings()
soup = BeautifulSoup(html, "html.parser")

cars = []
for listing in soup.select("div.vehicle-card")[:10]:
    try:
        title = listing.select_one("h2.vehicle-title").text.strip()
        price = listing.select_one("span.price").text.strip()
        location = listing.select_one("div.vehicle-location").text.strip()
        image = listing.select_one("img")["src"]
        link = "https://classiccars.com" + listing.select_one("a.vehicle-card-link")["href"]
        cars.append({
            "title": title,
            "price": price,
            "location": location,
            "image": image,
            "link": link
        })
    except Exception:
        continue

today = datetime.now().strftime("%Y-%m-%d")
html_out = f"""<!DOCTYPE html>
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
