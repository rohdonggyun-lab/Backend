# FastAPI + Pydantic 실무 과제 

> **사용하는 개념 **
> - `@app.get` / `@app.post` / `@app.put` 라우팅
> - 경로 매개변수 `/{item_id}`, 쿼리 매개변수 `skip`, `limit`
> - Pydantic `BaseModel`, 타입(`str`, `int`, `float`, `bool`), `Optional`, 기본값
> - `model_dump()`로 모델 → 딕셔너리 변환, 딕셔너리 return → JSON 응답

> **테스트 방법**
> 1. 과제 폴더에서 `uvicorn main:app --reload` 실행
> 2. 브라우저에서 **http://127.0.0.1:8000/docs** 접속
> 3. 해당 API → **Try it out** → 요청 JSON 입력 → **Execute**
> 4. 응답 코드(200 / 422)와 응답 JSON이 **예상 결과**와 같은지 확인

---

## 과제 1. 메모 등록 API 만들기 ⭐

**상황**
"마이 메모 앱"에 메모를 저장하는 기능을 만들어야 합니다. 프론트엔드 개발자가 메모를 JSON으로 보내면, 서버는 형식이 맞는지 확인하고 받은 메모를 그대로 돌려줘야 합니다.

**요구사항**

- `Memo` 모델을 만드세요.

| 필드 | 타입 | 필수 여부 | 기본값 |
|---|---|---|---|
| title | 문자열 | 필수 | - |
| content | 문자열 | 필수 | - |
| is_important | 불리언 | 선택 | None |

- `POST /memos/` 를 만들고 `{"memo": 메모 데이터}` 형태로 응답하세요.

**테스트 요청 및 예상 결과**

① 정상 요청

```json
{"title": "장보기", "content": "우유, 계란 사기", "is_important": true}
```

```json
200 → {"memo": {"title": "장보기", "content": "우유, 계란 사기", "is_important": true}}
```

② is_important 생략

```json
{"title": "회의록", "content": "주간 회의 정리"}
```

```json
200 → {"memo": {"title": "회의록", "content": "주간 회의 정리", "is_important": null}}
```

③ title 누락

```json
{"content": "제목 없음"}
```

```json
422 → "loc": ["body", "title"], "msg": "Field required"
```

**생각해 보기**: ③에서 우리는 검사 코드를 한 줄도 쓰지 않았습니다. 누가 막아 준 걸까요?

---

## 과제 2. 회원가입 API — 비밀번호는 돌려주지 않기 ⭐⭐

**상황**
회원가입 요청에는 비밀번호가 포함됩니다. 실무에서는 **비밀번호를 응답에 절대 포함하면 안 됩니다.** (로그, 브라우저 개발자 도구 등에 노출될 수 있기 때문)

**요구사항**

- `UserSignup` 모델을 만드세요.

| 필드 | 타입 | 필수 여부 | 기본값 |
|---|---|---|---|
| username | 문자열 | 필수 | - |
| email | 문자열 | 필수 | - |
| password | 문자열 | 필수 | - |
| age | 정수 | 필수 | - |
| marketing_agree | 불리언 | 선택 | False |

- `POST /users/signup` 을 만드세요.
- 응답에는 환영 메시지와 사용자 정보를 담되, **password는 빼고** 돌려주세요.
  (힌트: `user.username`처럼 필요한 값만 꺼내 딕셔너리를 직접 만드세요)

**테스트 요청 및 예상 결과**

① 정상 요청

```json
{"username": "hong", "email": "hong@example.com", "password": "pass1234", "age": 25}
```

```json
200 → {
  "message": "hong님, 가입을 환영합니다!",
  "user": {"username": "hong", "email": "hong@example.com", "age": 25, "marketing_agree": false}
}
```

② age에 문자 입력

```json
{"username": "kim", "email": "kim@example.com", "password": "pw", "age": "스물"}
```

```json
422 → "loc": ["body", "age"], "msg": "Input should be a valid integer, ..."
```

**생각해 보기**: `marketing_agree`는 보내지 않았는데 응답에 `false`가 들어 있습니다. 왜 그럴까요?

---

## 과제 3. 쇼핑몰 주문 금액 계산 API ⭐⭐

**상황**
쇼핑몰에서 주문이 들어오면 서버가 **총 금액을 계산**해서 돌려줘야 합니다. 금액 계산은 클라이언트를 믿지 않고 서버에서 하는 것이 실무 원칙입니다.

**요구사항**

- `Order` 모델을 만드세요.

| 필드 | 타입 | 필수 여부 | 기본값 |
|---|---|---|---|
| product_name | 문자열 | 필수 | - |
| price | 실수 | 필수 | - |
| quantity | 정수 | 필수 | - |
| coupon_code | 문자열 | 선택 | None |

- `POST /orders/` 를 만드세요.
- 계산 규칙
  - `total_price` = price × quantity
  - coupon_code가 `"WELCOME10"`이면 `discount` = total_price의 10%, 아니면 0
  - `final_price` = total_price − discount
- 응답 형식: `product_name`, `quantity`, `total_price`, `discount`, `final_price`

**테스트 요청 및 예상 결과**

① 쿠폰 없음

```json
{"product_name": "키보드", "price": 30000, "quantity": 2}
```

```json
200 → {"product_name": "키보드", "quantity": 2, "total_price": 60000.0, "discount": 0, "final_price": 60000.0}
```

② 쿠폰 적용

```json
{"product_name": "키보드", "price": 30000, "quantity": 2, "coupon_code": "WELCOME10"}
```

```json
200 → {"product_name": "키보드", "quantity": 2, "total_price": 60000.0, "discount": 6000.0, "final_price": 54000.0}
```

③ 수량에 소수 입력

```json
{"product_name": "마우스", "price": 15000, "quantity": 1.5}
```

```json
422 → "loc": ["body", "quantity"], "msg": "Input should be a valid integer, got a number with a fractional part"
```

**생각해 보기**: price를 `30000`(정수)으로 보냈는데 `total_price`가 `60000.0`(실수)으로 나옵니다. 이유는 무엇일까요?

---

## 과제 4. 메모 수정 API (경로 매개변수 + 요청 바디) ⭐⭐

**상황**
이미 저장된 메모를 수정하는 기능입니다. **몇 번 메모인지는 주소(URL)** 로, **수정할 내용은 요청 바디(JSON)** 로 받습니다.

**요구사항**

- `MemoUpdate` 모델을 만드세요. (필드는 과제 1의 Memo와 같음)
- `PUT /memos/{memo_id}` 를 만드세요. `memo_id`는 정수입니다.
- 응답 형식: `{"memo_id": 번호, "updated_memo": 수정 내용}`

**테스트 요청 및 예상 결과**

① `PUT /memos/1`

```json
{"title": "장보기(수정)", "content": "우유, 계란, 빵 사기", "is_important": false}
```

```json
200 → {"memo_id": 1, "updated_memo": {"title": "장보기(수정)", "content": "우유, 계란, 빵 사기", "is_important": false}}
```

② `PUT /memos/abc` (바디는 아무 메모나)

```json
422 → "loc": ["path", "memo_id"], "msg": "Input should be a valid integer, ..."
```

**생각해 보기**: 과제 1~3의 에러는 `loc`가 `"body"`였는데, ②는 `"path"`입니다. 이 차이가 의미하는 것은 무엇일까요?

---

## 과제 5. 할 일(To-Do) 관리 API — 등록 · 목록 · 상세 조회 ⭐⭐⭐

**상황**
팀에서 간단한 할 일 관리 서비스를 만들기로 했습니다. 아직 데이터베이스가 없으므로 **파이썬 리스트에 저장**합니다. (서버를 재시작하면 데이터가 사라집니다)

**요구사항**

- `Todo` 모델을 만드세요.

| 필드 | 타입 | 필수 여부 | 기본값 |
|---|---|---|---|
| task | 문자열 | 필수 | - |
| priority | 정수 | 선택 | 3 |
| done | 불리언 | 선택 | False |

- 저장소: `todo_db = []` (리스트의 인덱스를 todo_id로 사용)
- 만들어야 할 API 3개

| API | 기능 | 응답 형식 |
|---|---|---|
| `POST /todos/` | 할 일을 todo_db에 추가 | `{"todo_id": 번호, "todo": 데이터}` |
| `GET /todos/?skip=0&limit=10` | 목록 조회 (skip개 건너뛰고 limit개 반환) | `{"total": 전체 개수, "todos": [...]}` |
| `GET /todos/{todo_id}` | 상세 조회. 없는 번호면 에러 메시지 반환 | `{"todo_id": 번호, "todo": 데이터}` 또는 `{"error": "N번 할 일이 없습니다."}` |

(힌트: 리스트 슬라이싱 `todo_db[skip : skip + limit]`)

**테스트 순서 및 예상 결과**

① `POST /todos/` 3번 실행

```json
{"task": "FastAPI 복습", "priority": 1}
{"task": "과제 제출"}
{"task": "운동하기", "priority": 5, "done": true}
```

```json
200 → {"todo_id": 0, "todo": {"task": "FastAPI 복습", "priority": 1, "done": false}}
200 → {"todo_id": 1, "todo": {"task": "과제 제출", "priority": 3, "done": false}}
200 → {"todo_id": 2, "todo": {"task": "운동하기", "priority": 5, "done": true}}
```

② `GET /todos/` → total 3, 3개 모두 반환

③ `GET /todos/?skip=1&limit=1`

```json
200 → {"total": 3, "todos": [{"task": "과제 제출", "priority": 3, "done": false}]}
```

④ `GET /todos/0`

```json
200 → {"todo_id": 0, "todo": {"task": "FastAPI 복습", "priority": 1, "done": false}}
```

⑤ `GET /todos/99`

```json
200 → {"error": "99번 할 일이 없습니다."}
```

**생각해 보기**

- ⑤는 에러 상황인데 응답 코드가 200입니다. 실무에서는 어떤 응답 코드가 더 적절할까요? (힌트: 404)
- 서버를 재시작(Ctrl+C 후 다시 실행)하고 `GET /todos/`를 호출하면 어떻게 되나요? 왜 그럴까요?

**도전 과제 (선택)**

- `PUT /todos/{todo_id}`로 할 일 수정, `DELETE /todos/{todo_id}`로 삭제 기능을 추가해 보세요.
- `GET /todos/page` 주소를 만들어 할 일 목록을 HTML 화면(Jinja2 템플릿)으로 보여 주세요.

---

## 제출 체크리스트

- [ ] 5개 과제 모두 `/docs`에서 예상 결과와 같은 응답이 나오는지 확인했다
- [ ] 422 에러 응답의 `loc`와 `msg`를 읽고 원인을 설명할 수 있다
- [ ] 각 과제의 "생각해 보기" 질문에 답을 작성했다
