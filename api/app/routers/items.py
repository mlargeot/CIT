from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from ..models.item import Item
from ..models.functions import list_to_dict, get_conversion_rate
import requests
import json

router = APIRouter(prefix='/items')

items = []

@router.get('/', status_code=200)
async def get_items():

    try:
        binance_response = requests.get("https://www.binance.com/api/v3/ticker/price")
    except:
        raise HTTPException(status_code=500, detail='Unable to get ticker price')

    try:
        convertion_rate = get_conversion_rate()
    except:
       raise HTTPException(status_code=500, detail='Unable to load conversion currency')

    try:
        for item in binance_response.json():
            newItem: Item = Item()
            newItem.symbol = item["symbol"]
            newItem.value_usd = item["price"]
            newItem.value_eur = str(float(item["price"]) * float(convertion_rate))
            items.append(newItem)
    except:
        raise HTTPException(status_code=500, detail='Error while loading json data')

    return list_to_dict(items)
