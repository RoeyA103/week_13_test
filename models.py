from pydantic import BaseModel , ConfigDict

class Terrorist(BaseModel):
    model_config = ConfigDict(extra="ignore")
    name:str
    location:str
    danger_rate:int