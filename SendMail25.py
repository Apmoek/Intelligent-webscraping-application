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

# === CONFIG ===
DB_PATH = "bitcoin_data.db"
TABLE = "prices_unix"
THRESHOLD_PERCENT = 25
LOOKBACK_HOURS = 24

EMAIL_FROM = AppSendingGmail
EMAIL_TO = AppReceivingGmail
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USER = AppSmTpUser
SMTP_PASS = AppPasswordGmail  # Use app password if using Gmail

# === DB Logic ===
def get_prices():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # Get latest price
    cur.execute(f"SELECT price, timestamp FROM {TABLE} ORDER BY timestamp DESC LIMIT 1")
    latest = cur.fetchone()
    if not latest:
        conn.close()
        return None, None

    latest_price, latest_ts = latest
    target_ts = latest_ts - (LOOKBACK_HOURS * 3600)

    # Get closest price at or before target timestamp
    cur.execute(f"SELECT price FROM {TABLE} WHERE timestamp <= ? ORDER BY timestamp DESC LIMIT 1", (target_ts,))
    result = cur.fetchone()
    conn.close()

    if result:
        old_price = result[0]
        return old_price, latest_price
    else:
        return None, latest_price

# === Alert Logic ===
def should_alert(old, new):
    if old == 0:
        return False, 0
    change = abs((new - old) / old) * 100
    return change >= THRESHOLD_PERCENT, change

# === Email Logic ===
def send_email(change, old, new):
    subject = f"⚠️ Bitcoin Alert: {change:.2f}% price change"
    body = f"""
    Bitcoin price has changed more than {THRESHOLD_PERCENT}% in the last {LOOKBACK_HOURS} hours.
    
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
        alert_needed, percent_change = should_alert(old_price, new_price)
        if alert_needed:
            send_email(percent_change, old_price, new_price)
        else:
            print(f"No alert. Price changed {percent_change:.2f}% in last {LOOKBACK_HOURS}h.")
