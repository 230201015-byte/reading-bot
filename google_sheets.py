import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

SHEET_NAME = "Reading Marathon"
DATA_SHEET_NAME = "sheet1"   # ❗ ЛИСТ ДЛЯ ВВОДА ДАННЫХ (ЗАКРЫТЫЙ)

scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive",
]

creds = ServiceAccountCredentials.from_json_keyfile_name(
    "credentials.json",
    scope
)

client = gspread.authorize(creds)
spreadsheet = client.open(SHEET_NAME)

# ⚠️ ЯВНО указываем лист
data_sheet = spreadsheet.worksheet(DATA_SHEET_NAME)

GENDER_MAP = {
    "Әлішер": "male",
    "Нұрхасан": "male",
    "Жаһид": "male",
    "Айша": "female",
    "Гүлайна": "female",
    "Әсем": "female",
}

def add_record(name: str, date_str: str, pages: str):
    gender = GENDER_MAP.get(name, "unknown")

    data_sheet.append_row([
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        name,
        gender,
        date_str,
        pages
    ], value_input_option="USER_ENTERED")
