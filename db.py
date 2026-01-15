from pymongo import MongoClient 
import os
from fastapi import HTTPException

MONGO_HOST = os.getenv("MONGO_HOST","mongo-0.mongo-service")
MONGO_PORT = os.getenv("MONGO_PORT" , 27017)
MONGO_USERNAME = os.getenv("MONGO_USERNAME" , "admin")
MONGO_PASSWORD = os.getenv("MONGO_PASSWORD","secretpass")
MONGO_DB = os.getenv("MONGO_DB","threat_db")
MONGO_AUTH_SOURCE = os.getenv("MONGO_AUTH_SOURCE","admin")

def save_contact_to_db(data: dict):
        try:
            client = MongoClient(
                host=MONGO_HOST,
                port=MONGO_PORT,
                username=MONGO_USERNAME,
                password=MONGO_USERNAME,
                authSource=MONGO_AUTH_SOURCE
            )
          
            db = client[MONGO_DB]

            collection = db['top_threats']

            result = collection.insert_one(data)
            print(f"Inserted ID: {result.inserted_id}")

        except Exception as e:
            raise HTTPException(status_code=503,detail="Database unavailable")
        