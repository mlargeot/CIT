import requests
from fastapi import HTTPException

def list_to_dict(items: list) -> dict:
    dict_items = {}
    i = 0
    for item in items:
        dict_items[i] = dict(item)
        i = i + 1
    return dict_items

def get_conversion_rate() -> str:
    try:
        conversion_request = "https://cdn.taux.live/api/latest.json"
        conversion_response = requests.get(conversion_request)
        convertion_rate = conversion_response.json()['rates']['EUR']
    except:
       raise HTTPException(status_code=500, detail='Unable to load conversion currency')
    return convertion_rate
