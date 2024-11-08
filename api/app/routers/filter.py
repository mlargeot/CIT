from fastapi import APIRouter, HTTPException, status
from ..models.item   import  FilterItem
from ..models.functions import get_conversion_rate
from ..db import db
import requests

router = APIRouter(
    prefix='/filter',
    tags=["filter"]
)

filtered_items = []

@router.get(
        '/',
        responses={
            status.HTTP_500_INTERNAL_SERVER_ERROR: {
                "description": "Unable to load API data.",
                "content": {"application/json": {
                    "example": {
                        "detail": "Unable to load ticker price."
                    }
                }}
            }
        },
        response_model=list[FilterItem]
)
def get_filtered_elm() -> list[FilterItem]:
    try:
        binance_response = requests.get("https://www.binance.com/api/v3/ticker/price")
    except:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Unable to load ticker price.")

    try:
        conversion_rate = get_conversion_rate()
    except:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Unable to load conversion currency.")

    for elm in binance_response.json():
        for filter_elm in filtered_items:
            if (elm['symbol'] == filter_elm.symbol):
                filter_elm.value_usd = elm['price']
                filter_elm.value_eur = str(float(elm['price']) * float(conversion_rate))
                continue
    return filtered_items


@router.post(
        '/{symbol}',
        status_code=201,
        responses={
            status.HTTP_404_NOT_FOUND: {
                "description": "Unknown symbol.",
                "content": {"application/json": {
                    "example": {
                        "detail": "Invalid Email and Password combination."
                    }
                }}
            },
            status.HTTP_500_INTERNAL_SERVER_ERROR: {
                "description": "Unable to load API data.",
                "content": {"application/json": {
                    "example": {
                        "detail": "Unable to load ticker price."
                    }
                }}
            }
        },
        response_model=list[FilterItem]
)
def add_filter_elm(symbol: str):
    # TODO: LOAD FILTER LIST BASED ON DATABASE ELEMENTS

    try:
        binance_request = "https://www.binance.com/api/v3/ticker/price?symbol=" + symbol
        binance_response = requests.get(binance_request)
    except:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Unable to load ticker price.")

    try:
        conversion_rate = get_conversion_rate()
    except:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Unable to load conversion currency.")

    newItem: FilterItem = FilterItem()
    try:
        newItem.symbol = binance_response.json()['symbol']
        newItem.value_usd = binance_response.json()['price']
        newItem.value_eur = str(float(binance_response.json()['price']) * float(conversion_rate))
    except:
        raise HTTPException(status_code=404, detail='Unknown symbol')

    newItemDict = {
        "symbol": newItem.symbol,
        "value_usd": newItem.value_usd,
        "value_eur": newItem.value_eur
    }

    result = db.filter.find_one_and_update(
        {"symbol": newItem.symbol},
        {"$set": newItemDict},
        {"_id": False,
         "symbol": True}
    )

    if result is None:
        db.filter.insert_one(newItemDict)
        filtered_items.append(newItem)

    return filtered_items


@router.delete(
        '/{symbol}',
        status_code=200,
        response_model=list[FilterItem]
)
def remove_filter_elm(symbol: str):
    global filtered_items
    filtered_items = [item for item in filtered_items if item.symbol != symbol]
    return filtered_items
