import os
import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

# ================== CONFIG ==================
SHEET_NAME = "Reading Marathon"
DATA_SHEET_NAME = "sheet1"

# ================== AUTH ==================
creds_json = os.environ.get("GOOGLE_CREDENTIALS")
if not creds_json:
    raise Exception("❌ GOOGLE_CREDENTIALS не задана!")

try:
    creds_dict = json.loads(creds_json)
except json.JSONDecodeError:
    raise Exception("❌ GOOGLE_CREDENTIALS содержит невалидный JSON!")

scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive",
]

creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
client = gspread.authorize(creds)
spreadsheet = client.open(SHEET_NAME)
data_sheet = spreadsheet.worksheet(DATA_SHEET_NAME)

# ================== DATA ==================
GENDER_MAP = {
    "Әлішер": "male",
    "Нұрхасан": "male",
    "Жаһид": "male",
    "Айша": "female",
    "Гүлайна": "female",
    "Әсем": "female",
}

# ================== FUNCTIONS ==================
def add_record(name: str, date_str: str, pages: int):
    gender = GENDER_MAP.get(name, "unknown")
    data_sheet.append_row([
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        name,
        gender,
        date_str,
        pages
    ], value_input_option="USER_ENTERED")
