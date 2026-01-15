from fastapi import FastAPI ,UploadFile ,HTTPException
import pandas as pd
import shutil
import uvicorn
from db import save_contact_to_db
from models import Terrorist

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
    terrorist_list = df_to_list_dict(df)
    valid_list = basemodel_validation(terrorist_list)
    res = res_format(valid_list)

    save_contact_to_db(df.to_json())
    return res


    

def validation(file):
    if not file:
        raise HTTPException(status_code=400,detail="No file provided")
    if not file.filename.lower().endswith(('.csv',".xlsx",".xls")):
        raise HTTPException(status_code=400,detail="Invalid CSV file")
    
def save_csv_local(file):
    filepath = f"/tmp/{file.filename}"

    with open(filepath, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

def load_file(file_name:str):
    if file_name.endswith(".csv"):
        df = pd.read_csv(f"/tmp/{file_name}")
    else:
        df = pd.read_excel(f"/tmp/{file_name}")
    return df

def data_manipulation(df):
    df.sort_values(by="danger_rate",ascending=False,inplace=True)
    df = df.head(n=5)
    df = df[["name","location","danger_rate"]]
    return df

def df_to_list_dict(df):
    terror = []
    for col in df.values:
        a= {}
        a["name"] = col[0]
        a["location"] = col[1]
        a["danger_rate"] = col[2]
        terror.append(a)
    return terror    

def basemodel_validation(terrorists:list[dict]):
    res = []
    for terrorist in terrorists:
        try:
            Terrorist(**terrorist)
            res.append(terrorist)
        except Exception:
            pass
    return res    


def res_format(terrorists:list[dict]):
    count = len(terrorists)
    res = {"count":count,"top":terrorists}
    return res

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0",port=8000 , reload=True)