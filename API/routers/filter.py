from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
from models.item import Item
from models.functions import list_to_dict
import requests
import json

router = APIRouter(prefix='/filter')

filtered_items = []


@router.get('/')
async def get_filtered_elm():
  try:
      return list_to_dict(filtered_items)
  except:
    raise HTTPException(status_code=500, detail='Unable to load filtered items')


@router.post('/{symbol}', status_code=200)
async def add_filter_elm(symbol: str):
    try:
        binance_request = "https://www.binance.com/api/v3/ticker/price?symbol=" + symbol
        binance_response = requests.get(binance_request)
        print(binance_response.content)
    except:
        raise HTTPException(status_code=500, detail='Unable to load ticker price')

    try:
        conversion_request = "https://cdn.taux.live/api/latest.json"
        conversion_response = requests.get(conversion_request)
        convertion_rate = conversion_response.json()['rates']['EUR']
    except:
        raise HTTPException(status_code=500, detail='Unable to load conversion currency')

    newItem: Item = Item()
    try:
        newItem.symbol = binance_response.json()['symbol']
    except:
        raise HTTPException(status_code=404, detail='Unknown symbol')
    newItem.value_usd = binance_response.json()['price']
    newItem.value_eur = str(float(binance_response.json()['price']) * float(convertion_rate))
    
    for elm in filtered_items:
        if (elm.symbol == newItem.symbol):
            elm.value_usd = newItem.value_usd
            elm.value_eur = newItem.value_eur
            return list_to_dict(filtered_items)        

    filtered_items.append(newItem)
    return list_to_dict(filtered_items)


@router.delete('/{symbol}', status_code=200)
async def remove_filter_elm(symbol: str):
    global filtered_items
    filtered_items = [item for item in filtered_items if item.symbol != symbol]
    return list_to_dict(filtered_items)
