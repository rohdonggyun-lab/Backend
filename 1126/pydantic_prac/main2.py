# main2.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

# 임시 저장소 (서버가 재시작되면 사라집니다)
items_db: dict[int, dict] = {}
next_id = 1


class Item(BaseModel):
    name: str                          # 필수
    description: Optional[str] = None  # 선택, 기본값 None
    price: float                       # 필수
    tax: float = 0.1                   # 선택, 기본값 0.1


class ItemUpdate(BaseModel):
    # PATCH용: 모든 필드가 선택 (보낸 것만 수정)
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    tax: Optional[float] = None


@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI"}


# CREATE (POST): 생성
@app.post("/items/", status_code=201)
async def create_item(item: Item):
    global next_id
    items_db[next_id] = item.model_dump()
    created = {"id": next_id, **items_db[next_id]}
    next_id += 1
    return {"item": created}


# READ (GET): 목록 조회 (쿼리 파라미터)
@app.get("/items/")
def read_items(skip: int = 0, limit: int = 10):
    all_items = [{"id": k, **v} for k, v in items_db.items()]
    return {"items": all_items[skip: skip + limit], "total": len(all_items)}


# READ (GET): 단건 조회 (경로 파라미터)
@app.get("/items/{item_id}")
def read_item(item_id: int):
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"item": {"id": item_id, **items_db[item_id]}}


# UPDATE (PUT): 전체 교체
@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    items_db[item_id] = item.model_dump()
    return {"item": {"id": item_id, **items_db[item_id]}}


# UPDATE (PATCH): 부분 수정
@app.patch("/items/{item_id}")
def patch_item(item_id: int, item: ItemUpdate):
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    changes = item.model_dump(exclude_unset=True)  # 보낸 필드만
    items_db[item_id].update(changes)
    return {"item": {"id": item_id, **items_db[item_id]}}


# DELETE: 삭제
@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    del items_db[item_id]
    return {"message": f"Item {item_id} has been deleted"}

# 실행: python -m uvicorn main2:app --reload