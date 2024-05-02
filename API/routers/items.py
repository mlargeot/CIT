from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from models.item import Item
from models.functions import list_to_dict
import requests
import json

router = APIRouter(prefix='/items')

items = []

@router.get("/")
def get_items():
    return list_to_dict(items)
