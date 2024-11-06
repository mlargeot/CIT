from pymongo import MongoClient
import os

if os.getenv('DB_USER') and os.getenv('DB_PASS'):
    uri = f"mongodb://{os.getenv('DB_USER')}:{os.getenv('DB_PASS')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/"
    print(f"Connecting to mongodb://***:***@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/")
else:
    uri = f"mongodb://{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/"
    print("Connecting to", uri)

client = MongoClient(uri)
db = client.cit
