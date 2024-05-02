import sys
import requests

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
