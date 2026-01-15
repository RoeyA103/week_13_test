from fastapi import FastAPI ,UploadFile ,HTTPException
import pandas as pd
import shutil
import uvicorn

app = FastAPI()

@app.get("/")
def root():
    return {"message: healthy"}

@app.post("/top-threats")
def get_csv_file(file: UploadFile):
    validation(file=file)
    save_csv_local(file)
    df = load_file(file.filename)
    df = data_manipulation(df)
    # save_contact_to_db(df.to_json())
    return df.to_json()


    

def validation(file):
    if not file:
        raise HTTPException(status_code=400,detail="No file provided")
    if not file.filename.lower().endswith(('.csv',".xlsx",".xls")):
        raise HTTPException(status_code=400,detail="Invalid CSV file")
    
def save_csv_local(file):
    filepath = file.filename

    with open(filepath, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

def load_file(file_name:str):
    if file_name.endswith(".csv"):
        df = pd.read_csv(file_name)
    else:
        df = pd.read_excel(file_name)
    return df

def data_manipulation(df):
    df.sort_values(by="danger_rate",ascending=False,inplace=True)
    df = df.head(n=5)
    df = df[["name","location","danger_rate"]]
    return df


#--------------------------------------------------
from pymongo import MongoClient 
import os

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
        


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0",port=8000 , reload=True)