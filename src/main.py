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

def update_excel() -> bool:
        
    try:
        load_dotenv()
    except:
        return False

    try:
        scope = ['https://www.googleapis.com/auth/spreadsheets', "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
        credentials = ServiceAccountCredentials.from_json_keyfile_name(os.getenv('CREDS_FILE'), scope)
        client = gspread.authorize(credentials)
        google_sheet = client.open(os.getenv('SHEET_NAME')).sheet1
    except:
        return False

    try:
        filter_content = requests.get('http://127.0.0.1:8000/api/filter/')
    except:
        return False

    try:
        col = 2
        row = 2
        for elm in filter_content.json():
            google_sheet.update_cell(row, col, str(filter_content.json()[elm]['symbol']))
            google_sheet.update_cell(row + 1, col, float(filter_content.json()[elm]['value_usd']))
            google_sheet.update_cell(row + 2, col, float(filter_content.json()[elm]['value_eur']))
            col += 1
    except:
        return False

    try:
        clear = True
        col = len(filter_content.json()) + 2
        while(clear):
            if (google_sheet.cell(row, col).value == ''):
                clear = False
            else:
                google_sheet.update_cell(row, col, '')
                google_sheet.update_cell(row + 1, col, '')
                google_sheet.update_cell(row + 2, col, '')
                col += 1
    except:
        return False
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
