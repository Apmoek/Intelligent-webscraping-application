# Importeer vanuit het config bestand
from config import AppPasswordGmail
from config import AppReceivingGmail
from config import AppSendingGmail
from config import AppSmTpUser

# Importeer python libs
import sqlite3
import smtplib
from email.mime.text import MIMEText
from datetime import datetime, timedelta

# === Configuratie, dit zijn de variablen die terug komen in het script ===
DB_PATH = "bitcoin_data.db"
TABLE = "prices_unix"
THRESHOLD_PERCENT = 25
LOOKBACK_HOURS = 24
EMAIL_FROM = AppSendingGmail
EMAIL_TO = AppReceivingGmail
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USER = AppSmTpUser
SMTP_PASS = AppPasswordGmail  

# === Database onderdeel van het script ===
def get_prices():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # Haal de laatste prijs op
    cur.execute(f"SELECT price, timestamp FROM {TABLE} ORDER BY timestamp DESC LIMIT 1")
    latest = cur.fetchone()
    if not latest:
        conn.close()
        return None, None

    latest_price, latest_ts = latest
    target_ts = latest_ts - (LOOKBACK_HOURS * 3600)

    # Haal de meest recente prijs op sinds het script. 
    cur.execute(f"SELECT price FROM {TABLE} WHERE timestamp <= ? ORDER BY timestamp DESC LIMIT 1", (target_ts,))
    result = cur.fetchone()
    conn.close()

    if result:
        old_price = result[0]
        return old_price, latest_price
    else:
        return None, latest_price

# === Onderdeel voor de Alert ===
def should_alert(old, new):
    if old == 0:
        return False, 0
    change = abs((new - old) / old) * 100
    return change >= THRESHOLD_PERCENT, change

# === Onderdeel waarin de Email wordt geconfigureerd ===
def send_email(change, old, new):
    direction = "increased 📈" if new > old else "decreased 📉"
    subject = f"⚠️ Bitcoin Alert: Price {direction} by {change:.2f}%"
    
    body = f"""
    Bitcoin price has {direction} in the last {LOOKBACK_HOURS} hours.
    
    Old price: ${old:,.2f}
    New price: ${new:,.2f}
    Change: {change:.2f}%
    """

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = EMAIL_FROM
    msg["To"] = EMAIL_TO

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(SMTP_USER, SMTP_PASS)
        server.send_message(msg)

    print("✅ Alert email sent.")


# === Main ===
if __name__ == "__main__":
    old_price, new_price = get_prices()

    if old_price is None:
        print("❌ Not enough historical data to compare.")
    else:
        percent_change = abs((new_price - old_price) / old_price) * 100
        print(f"ℹ️ Sending test email. Price changed {percent_change:.2f}% in last {LOOKBACK_HOURS}h.")
        send_email(percent_change, old_price, new_price)
