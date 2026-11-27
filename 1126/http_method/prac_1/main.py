from fastapi import FastAPI
app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI"}


#경로 파라메터 /items/1     /items/2     /users/123
#/users/123/items/foobar
@app.get("/items/")
def read_items(skip=0, limit=10):
    return {"skip": skip, "limit": limit}

#쿼리 파라메터
# @app.get("/users/{user_id}/items/{item_name}")
# def read_item(user_id,item_id):
#     return {"user_id": user_id, "item_name":item_id}

