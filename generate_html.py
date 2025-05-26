from datetime import datetime

today = datetime.now().strftime("%Y-%m-%d")
html = f"""
<!DOCTYPE html>
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
  <h1>Classic Cars for Sale – {today}</h1>

  <div class="car">
    <img src="https://via.placeholder.com/600x300?text=1969+Camaro+SS" alt="1969 Camaro SS">
    <h2>1969 Camaro SS</h2>
    <p><strong>Price:</strong> $49,000<br>
    <strong>Location:</strong> Detroit, MI<br>
    <a href="#">View listing</a></p>
  </div>
</body>
</html>
"""

with open("index.html", "w") as f:
    f.write(html)
