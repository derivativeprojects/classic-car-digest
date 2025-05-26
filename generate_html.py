import requests
from bs4 import BeautifulSoup
from datetime import datetime

# URL of ClassicCars search results
URL = "https://classiccars.com/listings/find/all-years/all-makes/all-models?sort=recently-listed"

# Make the request
headers = {"User-Agent": "Mozilla/5.0"}
response = requests.get(URL, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")

# Parse the top 10 listings
cars = []
for listing in soup.select("div.vehicle-card")[:10]:
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

#
