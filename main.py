from fastapi import FastAPI ,UploadFile ,HTTPException , File
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
def get_csv_file(file: UploadFile = File(...)):
    validation(file=file)
    save_csv_local(file)
    df = load_file(file.filename)
    
    df = data_manipulation(df)
    valid_df = basemodel_validation(df)
    res = res_format(valid_df)
    save_contact_to_db(valid_df)
    return res


    

def validation(file:UploadFile):
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
    return df
   

def basemodel_validation(df:pd.DataFrame):
    valid = []
    for idx , row in df.iterrows():
        try:
            model = Terrorist(**row.to_dict())
            valid.append(model)
        except:
            pass
    df = pd.DataFrame([m.model_dump() for m in valid])
    return df


def res_format(df:pd.DataFrame):
    count = len(df)
    res = {"count":count,"top":df.to_dict(orient="records")}
    return res

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0",port=8000 , reload=True)