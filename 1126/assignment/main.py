from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# ---------- 과제 1. 메모 등록 API 만들기 ⭐ ----------
class Memo(BaseModel):
    title: str
    content: str
    is_important: Optional[bool] = None

@app.post("/memos/")
def create_memo(memo: Memo):
    return {"memo": memo.model_dump()}

#생각해 보기: ③에서 우리는 검사 코드를 한 줄도 쓰지 않았습니다. 누가 막아 준 걸까요?
# Memo 클래스에 BaseModel파라메터를 지정했기 때문에 FastAPI가 작동하여 막아주었습니다.


# ---------- 과제 2. 회원가입 API — 비밀번호는 돌려주지 않기) ----------
class UserSignup(BaseModel):
    username: str
    email: str
    password: str
    age: int
    marketing_agree: bool = False

@app.post("/users/signup")
def signup(user: UserSignup):
    return {
        "message": f"{user.username}님, 가입을 환영합니다!",
        "user": {
            "username": user.username,
            "email": user.email,
            "age": user.age,
            "marketing_agree": user.marketing_agree,
        },
    }

#생각해 보기: marketing_agree는 보내지 않았는데 응답에 false가 들어 있습니다. 왜 그럴까요?
# Usersignup 클래스에 marketing_agree가 기본값으로 False되어있기 때문입니다.

# ---------- 과제 3. 쇼핑몰 주문 금액 계산 API ⭐⭐ ----------
class Order(BaseModel):
    product_name: str
    price: float
    quantity: int
    coupon_code: Optional[str] = None


@app.post("/orders/")
def create_order(order: Order):
    total_price = order.price * order.quantity
    discount = total_price * 0.1 if order.coupon_code == "WELCOME10" else 0
    return {
        "product_name": order.product_name,
        "quantity": order.quantity,
        "total_price": total_price,
        "discount": discount,
        "final_price": total_price - discount,
    }

#생각해 보기: price를 30000(정수)으로 보냈는데 total_price가 60000.0(실수)으로 나옵니다. 이유는 무엇일까요?
# Order 클래스에 price를 float로 설정했기 때문입니다.

# ---------- 과제 4. 메모 수정 API (경로 매개변수 + 요청 바디) ⭐⭐) ----------
class MemoUpdate(BaseModel):
    title: str
    content: str
    is_important: Optional[bool] = None


@app.put("/memos/{memo_id}")
def update_memo(memo_id: int, memo: MemoUpdate):
    return {"memo_id": memo_id, "updated_memo": memo.model_dump()}

#생각해 보기: 과제 1~3의 에러는 loc가 "body"였는데, ②는 "path"입니다. 이 차이가 의미하는 것은 무엇일까요?
# loc는 에러가 난 위치를 알려줍니다. 과제 1~3의 에러는 body 과제 4의 2는 path(주소)에서 에러가 났습니다.

# ---------- 과제 5. 할 일(To-Do) 관리 API — 등록 · 목록 · 상세 조회 ⭐⭐⭐ ----------
class Todo(BaseModel):
    task: str
    priority: Optional[int] = 3
    done: Optional[bool] = False

todo_db = []

@app.post("/todos/")
def create_todo(todo: Todo):
    todo_db.append(todo.model_dump())
    return {"todo_id": len(todo_db) - 1, "todo": todo_db[-1]}

@app.get("/todos/")
def list_todos(skip: int = 0, limit: int = 10):
    return {"total": len(todo_db), "todos": todo_db[skip : skip + limit]}

@app.get("/todos/{todo_id}")
def get_todo(todo_id: int):
    if 0 <= todo_id < len(todo_db):
        return {"todo_id": todo_id, "todo": todo_db[todo_id]}
    return {"error": f"{todo_id}번 할 일이 없습니다."}

#생각해 보기
#⑤는 에러 상황인데 응답 코드가 200입니다. 실무에서는 어떤 응답 코드가 더 적절할까요? (힌트: 404)
# 404 Not Found가 적절합니다. HTTP 상태 코드는 클라이언트가 성공 여부를 판단하는 표준 신호입니다. 에러인데 200을 주면 클라이언트가 응답 본문을 일일이 열어 error 키가 있는지 확인해야 합니다. 

#서버를 재시작(Ctrl+C 후 다시 실행)하고 GET /todos/를 호출하면 어떻게 되나요? 왜 그럴까요?
# 등록했던 할 일이 모두 사라집니다. todo_db = []는 서버 프로세스의 메모리에만 있는 파이썬 변수이기 때문입니다.