import os
import sys
import requests
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from dotenv import load_dotenv

def add_filter_elm(symbol: str) -> bool:
    try:
        full_request = "http://127.0.0.1:8000/api/filter/" + symbol
        requests.post(full_request)
    except:
        return False
    return True

def del_filter_elm(symbol: str) -> bool:
    try:
        full_request = "http://127.0.0.1:8000/api/filter/" + symbol
        requests.delete(full_request)
    except:
        return False
    return True

def set_filter_to_map(filter_elms) -> list[list]:
    elm_map = [[], [], []]
    for elm in filter_elms:
        elm_map[0].append(str(filter_elms[elm]['symbol']))
        elm_map[1].append(float(filter_elms[elm]['value_usd']))
        elm_map[2].append(float(filter_elms[elm]['value_eur']))
    return elm_map


def to_col(number):
    letter = ''
    while number > 26:
        letter += chr(ord("A") + int((number - 1) / 26) - 1)
        number = number - int((number - 1) / 26) * 26
    letter += chr(ord("A") - 1 + number)
    return letter


def update_excel() -> bool:

    load_dotenv()

    scope = ['https://www.googleapis.com/auth/spreadsheets', "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
    credentials = ServiceAccountCredentials.from_json_keyfile_name(os.getenv('CREDS_FILE'), scope)
    client = gspread.authorize(credentials)
    google_sheet = client.open(os.getenv('SHEET_NAME')).sheet1

    filter_content = requests.get('http://127.0.0.1:8000/api/filter/')

    filter_map = set_filter_to_map(filter_content.json())

    nb_symbol = len(filter_map[0]) + 1
    letter = to_col(nb_symbol)
    google_sheet.update(filter_map, f"B2:{letter}4")
    
    last_col = len(google_sheet.row_values(2))

    if nb_symbol != last_col:
        google_sheet.batch_clear([f"{to_col(nb_symbol + 1)}2:{to_col(last_col + 1)}4"])

    return True

def main():
    if (len(sys.argv) > 1):
        match (sys.argv[1]):
            case "add":
                return add_filter_elm(sys.argv[2])
            case "del":
                return del_filter_elm(sys.argv[2])
            case _:
                print("Invalid option")
                return False
    elif (len(sys.argv) == 1):
        update_excel()
    else:
        print("Invalid option")
        return

if __name__ == '__main__':
    main()
