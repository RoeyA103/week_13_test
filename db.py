from pymongo import MongoClient, errors
import os
from fastapi import HTTPException

MONGO_HOST = os.getenv("MONGO_HOST")
MONGO_PORT = int(os.getenv("MONGO_PORT"))
MONGO_USERNAME = os.getenv("MONGO_USERNAME")
MONGO_PASSWORD = os.getenv("MONGO_PASSWORD")
MONGO_DB = os.getenv("MONGO_DB")
MONGO_AUTH_SOURCE = os.getenv("MONGO_AUTH_SOURCE")

def save_contact_to_db(df):
    client = None
    try:
        client = MongoClient(
            host=MONGO_HOST,
            port=MONGO_PORT,
            username=MONGO_USERNAME,
            password=MONGO_PASSWORD,
            authsource=MONGO_AUTH_SOURCE
        )

        db = client[MONGO_DB]
        collection = db["top_threats"]

        # If df has multiple rows
        result = collection.insert_many(df.to_dict(orient="records"))
        return result.inserted_ids

    except errors.PyMongoError as e:
        raise HTTPException(status_code=503, detail=str(e))

   
