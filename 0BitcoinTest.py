# Importing variables from config file
from config import api_key, ticker, currency

# Importing Python libs
import requests
import pandas as pd  # New import

# Main code to retrieve actual Bitcoin price
url = f"https://api.coingecko.com/api/v3/simple/price?ids={ticker}&vs_currencies={currency}&x_cg_demo_api_key={api_key}"
headers = {"accept": "application/json"}
response = requests.get(url, headers=headers)

# Convert response to JSON
data = response.json()

# Create a DataFrame
df = pd.DataFrame([{
    "ticker": ticker,
    "currency": currency,
    "price": data[ticker][currency],
    "source": "CoinGecko"
}])

# Export to CSV
df.to_csv("bitcoin_price.csv", index=False)

print("✅ Data saved to bitcoin_price.csv")