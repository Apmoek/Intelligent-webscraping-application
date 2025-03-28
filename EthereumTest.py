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

