import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json
import os
from pathlib import Path

# === Config ===
CREDENTIALS_PATH = "credentials.json"   # Path of credentials
SHEET_NAME = "Stock Portfolio"            # GoogleSheet
WORKSHEET_NAME = "Report"                 # Worksheet
JSON_OUTPUT_PATH = "portfolio.json"     # Output json (in add-on: /share/portfolio.json)

# === Google Sheets API authentication ===
scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive.readonly"
]

try:
    creds = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_PATH, scope)
    client = gspread.authorize(creds)
except Exception as e:
    print(f"Authentication error: {e}")
    exit(1)

# === Reading Google Sheets ===
try:
    sheet = client.open(SHEET_NAME).worksheet(WORKSHEET_NAME)
    data = sheet.get_all_values()
except Exception as e:
    print(f"Google Sheet reading error: {e}")
    exit(1)

# === Processing the data ===
headers = data[0]
rows = data[1:]

portfolio_entries = []
for row in rows:
    try:
        portfolio_entries.append({
            "ticker": row[0].strip(),
            "deviza": row[3].strip(),
            "db": float(row[2].replace(",", ".").strip()),
            "buy_price": float(row[4].replace("Ft", "").replace(" ", "").replace(",", ".").strip()),
            "sell_price": float(row[5].replace("Ft", "").replace(" ", "").replace(",", ".").strip()),
            "gain_percent": float(row[6].replace("%", "").replace(",", ".").strip()),
            "gain_huf": float(row[7].replace("Ft", "").replace(" ", "").replace(",", ".").replace("-", "-").strip()),
            "weight_percent": float(row[8].replace("%", "").replace(",", ".").strip())
        })
    except Exception as e:
        print(f"Error in row: {row} > {e}")

# === New snapshot with TimeStamp ===
snapshot = {
    "timestamp": datetime.now().isoformat(),
    "portfolio": portfolio_entries
}

# === Parse the existing portfolio.json ===
if os.path.exists(JSON_LOG_PATH):
    with open(JSON_LOG_PATH, "r") as f:
        try:
            existing_data = json.load(f)
        except json.JSONDecodeError:
            existing_data = []
else:
    existing_data = []

existing_data.append(snapshot)

# === Write the new data to portfolio.json ===
with open(JSON_LOG_PATH, "w") as f:
    json.dump(existing_data, f, indent=2)

print(f"Data is saved in {JSON_LOG_PATH} ")