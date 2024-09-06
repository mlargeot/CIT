import requests
from fastapi import HTTPException

def get_conversion_rate() -> str:
    try:
        conversion_request = "https://cdn.taux.live/api/latest.json"
        conversion_response = requests.get(conversion_request)
        convertion_rate = conversion_response.json()['rates']['EUR']
    except:
       raise HTTPException(status_code=500, detail='Unable to load conversion currency')
    return convertion_rate
