import sys
import requests
import gspread
from oauth2client.service_account import ServiceAccountCredentials

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
        scope = ['https://www.googleapis.com/auth/spreadsheets', "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
        credentials = ServiceAccountCredentials.from_json_keyfile_name('./test.json', scope)
        client = gspread.authorize(credentials)
        google_sheet = client.open('Testsheet').sheet1
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
    return True

def main():
    if (len(sys.argv) == 3):
        match (sys.argv[1]):
            case "add":
                return add_filter_elm(sys.argv[2])
            case "del":
                return del_filter_elm(sys.argv[2])
    elif (len(sys.argv) == 1):
        update_excel()
    else:
        print("Invalid option")
        return

if __name__ == '__main__':
    main()
