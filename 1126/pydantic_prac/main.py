# main.py
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

class Item(BaseModel):
    name: str
    price: float
    is_offer: Optional[bool] = None

@app.post("/items/")
def create_item(item: Item):
    return {"item": item.model_dump()}

# 실행: uvicorn main:app --reload