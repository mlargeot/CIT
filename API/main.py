from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

items = []
filtered_items = []

class Item(BaseModel):
    symbol: str = None
    value_eur: str = None
    value_usd: str = None

app.get("/")
def root():
    return items

app.get("/filter/")
def get_filtered_items():
    return filtered_items

app.post("/filter/{symbol}/")
def add_filter_elm(symbol: str):
    newItem: Item
    newItem.symbol = symbol
    filtered_items.append(newItem)
    return filtered_items

app.delete("/filter/{symbol}/")
def remove_filter_elm(symbol: str):
    global filtered_items
    filtered_items = [item for item in filtered_items if item.symbol != symbol]
    return filtered_items
