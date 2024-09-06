from uvicorn import run
from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from .routers import filter
from .routers import items

app = FastAPI()
router = APIRouter(prefix='/api')

router.include_router(items.router)
router.include_router(filter.router)

app.include_router(router)

app.add_middleware(
  CORSMiddleware,
  allow_origins=['*'],
  allow_credentials=True,
  allow_methods=['*'],
  allow_headers=['*']
)
