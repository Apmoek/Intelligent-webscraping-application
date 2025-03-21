# Importing variables from config file.
from config import api_key
from config import ticker
from config import currency

# Importing Python libs
import requests
import pandas as pd
from datetime import datetime
import os
import sqlite3

# Main code to retrieve actual Bitcoin price
url = f"https://api.coingecko.com/api/v3/simple/price?ids={ticker}&vs_currencies={currency}&x_cg_demo_api_key={api_key}"
headers = {"accept": "application/json"}
response = requests.get(url, headers=headers)

# Convert respone to JSON
data = response.json()

# Add timestamp
timestamp = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

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

# Create or append to SQLite database
conn = sqlite3.connect("bitcoin_data.db")
df.to_sql("prices", conn, if_exists="append", index=False)
conn.close()

# Terminal messag, when script has been completed.
print(f"✅ Data appended to {filename} and stored in bitcoin_data.db")











