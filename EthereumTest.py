# Importing variables from config file.
from config import api_key
from config import ticker1
from config import currency

# Importing Python libs
import requests
import pandas as pd
from datetime import datetime
import os
import sqlite3

# Main code to retrieve actual Ethereum price
url = f"https://api.coingecko.com/api/v3/simple/price?ids={ticker1}&vs_currencies={currency}&x_cg_demo_api_key={api_key}"
headers = {"accept": "application/json"}
response = requests.get(url, headers=headers)

# Convert respone to JSON
data = response.json()

# Add timestamp
timestamp = int(datetime.now().timestamp())  # Gives you Unix time as int

# Create a DataFrame
df = pd.DataFrame([{
    "timestamp": timestamp,
    "ticker": ticker1,
    "currency": currency,
    "price": data[ticker1][currency],
    "source": "CoinGecko"
}])

# Define filename
filename = "ethereum_price.csv"

# Check if file exists
file_exists = os.path.isfile(filename)

# Append to CSV file
df.to_csv(filename, mode='a', index=False, header=not file_exists)

# Create or append to SQLite database
conn = sqlite3.connect("bitcoin_data.db")
df.to_sql("prices_eth_unix", conn, if_exists="append", index=False)
conn.close()

# Terminal message, when script has been completed.
print(f"✅ Data appended to {filename} and stored in bitcoin_data.db in the prices_eth_unix table.")