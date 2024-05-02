from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
from models.item import Item
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

def list_to_dict(items: list) -> dict:
    dict_items = {}
    i = 0
    for item in items:
        dict_items[i] = dict(item)
        i = i + 1
    return dict_items

@router.post('/{symbol}', status_code=200)
async def add_filter_elm(symbol: str):

    newItem: Item = Item()
    newItem.symbol = symbol

    try:
        binance_request = "https://www.binance.com/api/v3/ticker/price?symbol=" + symbol
        binance_response = requests.get(binance_request)
        print(binance_response.content)
    except:
        raise HTTPException(status_code=404, detail='Unknown symbol')

    try:
        conversion_request = "https://cdn.taux.live/api/latest.json"
        conversion_response = requests.get(conversion_request)
    except:
       raise HTTPException(status_code=500, detail='Unable to load conversion currency')
    
    filtered_items.append(newItem)
    return list_to_dict(filtered_items)

@router.delete('/{symbol}', status_code=200)
async def remove_filter_elm(symbol: str):
    global filtered_items
    filtered_items = [item for item in filtered_items if item.symbol != symbol]
    return list_to_dict(filtered_items)
