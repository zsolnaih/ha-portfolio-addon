from collections import defaultdict
from datetime import date, datetime, timedelta
import re
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json
import os
from pathlib import Path
from zoneinfo import ZoneInfo

# def clean_number(value):
#     value = value.replace(",", ".")
#     return float(re.sub(r"[^\d\.\-]", "", value))

def reduce_snapshots(data):
    today = datetime.now().date()
    grouped = defaultdict(list)

    for entry in data:
        ts = datetime.fromisoformat(entry["timestamp"])
        grouped[ts.date()].append((ts, entry))

    reduced = []

    for day, items in grouped.items():
        timestamps = [ts for ts, _ in items]

        if day == today:
            # Mai nap: minden snapshot megmarad
            reduced.extend([entry for _, entry in items])

        elif day >= today - timedelta(days=7):
            # Elmúlt 7 nap: napi 2 snapshot (első és utolsó)
            reduced.append(min(items, key=lambda x: x[0])[1])
            reduced.append(max(items, key=lambda x: x[0])[1])

        elif day >= today - timedelta(days=30):
            # 1 hónap: heti 2 snapshot (hétfő + csütörtök)
            if timestamps[0].weekday() in (0, 3):
                reduced.append(min(items, key=lambda x: x[0])[1])

        elif day >= date(today.year, 1, 1):
            # YTD: heti 1 snapshot (hétfő)
            if timestamps[0].weekday() == 0:
                reduced.append(min(items, key=lambda x: x[0])[1])

    return sorted(reduced, key=lambda x: x["timestamp"])

# === Config ===
SHEET_NAME = "Stock Portfolio"            # GoogleSheet
WORKSHEET_NAME = "Report"                 # Worksheet
# JSON_OUTPUT_PATH = "/share/portfolio_log.json"    # Output json (in add-on: /share/portfolio.json)
# CREDENTIALS_PATH = "/share/credentials.json"  # Path of credentials

CREDENTIALS_PATH = "credentials.json"  # Path of credentials
JSON_OUTPUT_PATH = "portfolio_log.json"

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

summary = []
for row in rows:
    if not row[0].strip():
        try:
            summary.append({
                "portfolio_value": float(row[5].replace("Ft", "").replace("\xa0", "").replace(",", ".").strip()),
                "gain_percent": float(row[6].replace("%", "").replace(",", ".").strip())
            })
        except Exception as e:
            print(f"Error in row: {row} > {e}")


# === New snapshot with TimeStamp ===
snapshot = {
    # "timestamp": datetime.now().replace(second=0, microsecond=0).isoformat(),
    "timestamp": datetime.now(ZoneInfo("Europe/Budapest")).replace(second=0, microsecond=0).isoformat(),
    "portfolio_value": summary[0]["portfolio_value"],
    "gain_percent": summary[0]["gain_percent"]
}

# === Parse the existing portfolio.json ===
# if os.path.exists(JSON_OUTPUT_PATH):
#     with open(JSON_OUTPUT_PATH, "r") as f:
#         try:
#             existing_data = json.load(f)
#         except json.JSONDecodeError:
#             existing_data = []
# else:
#     existing_data = []

# existing_data.append(snapshot)

# === Cleaning policy ===
# reduced_data = reduce_snapshots(existing_data)

# === Write the new data to portfolio.json ===
with open(JSON_OUTPUT_PATH, "w") as f:
    json.dump(snapshot, f, indent=2)

print(f"Data is saved in {JSON_OUTPUT_PATH} ")