from pydantic import BaseModel

class Item(BaseModel):
    symbol: str = None
    value_eur: str = None
    value_usd: str = None
