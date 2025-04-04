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

# Code die een API verbinding maakt naar Coingecko om de prijs op te halen van Bitcoin.
url = f"https://api.coingecko.com/api/v3/simple/price?ids={ticker1}&vs_currencies={currency}&x_cg_demo_api_key={api_key}"
headers = {"accept": "application/json"}
response = requests.get(url, headers=headers)

# Zet het antwoord om in json.
data = response.json()

# Geeft de tijd aan
timestamp = int(datetime.now().timestamp())  # Wordt aangemaakt in unix formaat

# Geeft de data vorm die in de database komt.
df = pd.DataFrame([{
    "timestamp": timestamp,
    "ticker": ticker1,
    "currency": currency,
    "price": data[ticker1][currency],
    "source": "CoinGecko"
}])

# Geeft de naam aan van het CSV bestand. 
# filename = "ethereum_price.csv"

# Controleert of het bestand als bestaat.
# file_exists = os.path.isfile(filename)

# Stukje code wat een csv bestand maakt als het er nog niet is en anders een extra rij toevoegd aan het bestand. 
# df.to_csv(filename, mode='a', index=False, header=not file_exists)

# Maakt de database aan als deze niet bestaat, als dat wel zo is wordt er data bijgeschreven.
conn = sqlite3.connect("bitcoin_data.db")
df.to_sql("prices_eth_unix", conn, if_exists="append", index=False)
conn.close()

# Een terminal bericht dat het script succesvol heeft gedraaid.
print(f"✅ Data appended to and stored in bitcoin_data.db in the prices_eth_unix table.")