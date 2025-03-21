# Importing variables from config file
from config import api_key, ticker, currency

# Importing Python libs
import requests
import pandas as pd
from datetime import datetime
import os

# Main code to retrieve actual Bitcoin price
url = f"https://api.coingecko.com/api/v3/simple/price?ids={ticker}&vs_currencies={currency}&x_cg_demo_api_key={api_key}"
headers = {"accept": "application/json"}
response = requests.get(url, headers=headers)

# Convert response to JSON
data = response.json()

# Add timestamp
timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Create a DataFrame
df = pd.DataFrame([{
    "timestamp": timestamp,
    "ticker": ticker,
    "currency": currency,
    "price": data[ticker][currency],
    "source": "CoinGecko"
}])

# Define filename
filename = "bitcoin_price.csv"

# Check if file exists
file_exists = os.path.isfile(filename)

# Append to CSV file
df.to_csv(filename, mode='a', index=False, header=not file_exists)

print(f"✅ Data appended to {filename}")
