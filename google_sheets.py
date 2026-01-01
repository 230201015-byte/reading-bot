import os
import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

SHEET_NAME = "Reading Marathon"
DATA_SHEET_NAME = "sheet1"

SCOPE = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive",
]

GENDER_MAP = {
    "Әлішер": "male",
    "Нұрхасан": "male",
    "Жаһид": "male",
    "Айша": "female",
    "Гүлайна": "female",
    "Әсем": "female",
}

def get_data_sheet():
    creds_json = os.getenv("GOOGLE_CREDENTIALS")
    if not creds_json:
        raise Exception("❌ GOOGLE_CREDENTIALS не задана")

    try:
        creds_dict = json.loads(creds_json)
    except json.JSONDecodeError:
        raise Exception("❌ GOOGLE_CREDENTIALS содержит невалидный JSON")

    # вот это заменяет from_json_keyfile_name
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, SCOPE)
    client = gspread.authorize(creds)
    sheet = client.open(SHEET_NAME).worksheet(DATA_SHEET_NAME)
    return sheet

def add_record(name: str, date_str: str, pages: int):
    sheet = get_data_sheet()
    gender = GENDER_MAP.get(name, "unknown")
    sheet.append_row(
        [
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            name,
            gender,
            date_str,
            pages
        ],
        value_input_option="USER_ENTERED"
    )
