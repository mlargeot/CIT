from fastapi import APIRouter, HTTPException, status
from ..models.item import Item
from ..models.functions import get_conversion_rate
import requests

router = APIRouter(
    prefix='/items',
    tags=["items"]
)

items = []

@router.get('/',
            status_code=200,
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
            response_model=list[Item]
)
async def get_items() -> list[Item]:

    try:
        binance_response = requests.get("https://www.binance.com/api/v3/ticker/price")
    except:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Unable to load ticker price.")

    try:
        convertion_rate = get_conversion_rate()
    except:
       raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Unable to load conversion currency.")

    for item in binance_response.json():
        newItem: Item = Item()
        newItem.symbol = item["symbol"]
        newItem.value_usd = item["price"]
        newItem.value_eur = str(float(item["price"]) * float(convertion_rate))
        items.append(newItem)
    return items
