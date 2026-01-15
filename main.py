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
    df = df.head(5)



if __name__=="__main__":
   uvicorn.run("main:app", host="localhost",port=8000 , reload=True)
