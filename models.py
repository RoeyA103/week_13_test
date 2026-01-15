from pydantic import BaseModel

class Terrorist(BaseModel):
    name:str
    location:str
    danger_rate:int