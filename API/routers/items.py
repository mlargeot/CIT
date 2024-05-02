from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from models.item import Item
import requests
import json

router = APIRouter(prefix='/items')

items = []

@router.get("/")
def get_items():
    return items
