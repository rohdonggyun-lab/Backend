# FastAPI + MySQL 회원 관리 (PyMySQL 기본 연동)

---

## 학습 목표

- SQLAlchemy 없이 **PyMySQL**로 MySQL에 연결하고 SQL을 직접 실행할 수 있다.
- 회원가입 / 조회 / 비밀번호 수정 / 회원 탈퇴(CRUD)를 API와 HTML 화면으로 만들 수 있다.
- 휴대폰 번호를 **정규표현식**으로 검증하고, 비밀번호를 **bcrypt 해시**로 저장할 수 있다.
- **Postman**으로 API를 테스트하고 **MySQL에서 데이터 변화**를 확인할 수 있다.
- 한 파일(v1)을 **실무형 폴더 구조(v2)** 로 나눌 수 있다.

---

## 0. 전체 구성

### 0-1. 제공 파일

```
user_mysql/
├── 회원관리_MySQL_수업교안.md          ← 지금 이 문서
├── sql/schema.sql                      ← DB·테이블 생성 + 데이터 확인 SQL
├── postman/회원관리_API.postman_collection.json   ← Postman 가져오기용
└── student/                            ← 실습 (템플릿 + 작업 순서 주석)
    ├── v1/  main.py(TODO) + templates/
    └── v2/  main.py + app/(TODO) + templates/
```

> **실습 (/student) HTML 템플릿은 완성본**, 파이썬 코드는 **함수 틀 + STEP/TODO 주석**만 있습니다. 주석의 번호 순서대로 채우세요. 채우기 전에도 서버는 실행됩니다.

### 0-2. 기능과 주소

| 기능          | JSON API (Postman)                  | HTML 화면 (브라우저)             |
| ------------- | ----------------------------------- | -------------------------------- |
| 회원가입      | `POST /api/users`                   | `GET /signup` → `POST /signup`   |
| 목록 조회     | `GET /api/users`                    | `GET /`                          |
| 상세 조회     | `GET /api/users/{user_id}`          | `GET /users/{user_id}`           |
| 비밀번호 수정 | `PUT /api/users/{user_id}/password` | `POST /users/{user_id}/password` |
| 회원 탈퇴     | `DELETE /api/users/{user_id}`       | `POST /users/{user_id}/delete`   |

> 💡 **HTML 화면은 왜 PUT/DELETE가 아니라 POST일까?**
> HTML `<form>`은 **GET과 POST만** 보낼 수 있습니다. 그래서 화면용 수정·삭제는 POST + 별도 주소(`/password`, `/delete`)로 만듭니다.

### 0-3. 입력 규칙

| 항목        | 규칙                                    | 위반 시 |
| ----------- | --------------------------------------- | ------- |
| 이름        | 1~50자                                  | 422     |
| 휴대폰      | `^010-\d{4}-\d{4}$` (예: 010-1234-5678) | 422     |
| 비밀번호    | 8~20자                                  | 422     |
| 휴대폰 중복 | 같은 번호로 가입 불가 (DB UNIQUE)       | 409     |
| 본인 확인   | 수정·탈퇴 시 비밀번호 일치              | 401     |
| 없는 회원   | -                                       | 404     |

---

## 1. 환경 준비

### 1-1. MySQL 준비

- MySQL Server 8.x 실행 중인지 확인 (Windows: 서비스에서 `MySQL80` 실행 중)
- MySQL Workbench로 root 계정 접속 확인 → **root 비밀번호를 mysql1234 기억**해 둡니다.

### 1-2. 패키지 설치

```bash
pip install pymysql cryptography bcrypt python-multipart
```

| 패키지             | 용도                                                      |
| ------------------ | --------------------------------------------------------- |
| `pymysql`          | 파이썬 ↔ MySQL 연결 (순수 파이썬, 설치 쉬움)              |
| `cryptography`     | MySQL 8 기본 인증 방식(caching_sha2_password) 접속에 필요 |
| `bcrypt`           | 비밀번호 해시                                             |
| `python-multipart` | HTML `<form>` 데이터(Form) 받기                           |
| `jinja2`           | HTML 템플릿                                               |

(각 프로젝트 폴더의 `requirements.txt`로 `pip install -r requirements.txt` 해도 됩니다.)

### 1-3. DB·테이블 만들기

서버가 시작될 때 `init_db()`가 **DB와 테이블을 자동으로 만듭니다.** 수업에서는 SQL을 먼저 직접 실행해 보는 것을 권장합니다. (`sql/schema.sql`)

```sql
CREATE DATABASE IF NOT EXISTS fastapi_db
    DEFAULT CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE fastapi_db;

CREATE TABLE IF NOT EXISTS user (
    id         INT AUTO_INCREMENT PRIMARY KEY,   -- 회원 번호 (자동 증가)
    name       VARCHAR(50)  NOT NULL,            -- 이름
    phone      VARCHAR(13)  NOT NULL UNIQUE,     -- 휴대폰 (중복 불가)
    password   VARCHAR(255) NOT NULL,            -- bcrypt 해시 (60자)
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,                              -- 가입일
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP   -- 수정일 (자동 갱신)
);

DESC user;
```

| 컬럼                       | 포인트                                                                            |
| -------------------------- | --------------------------------------------------------------------------------- |
| `phone ... UNIQUE`         | 같은 번호를 두 번 넣으면 DB가 **IntegrityError**를 냄 → 중복 가입 409 처리에 사용 |
| `password VARCHAR(255)`    | 평문이 아니라 해시(`$2b$12$...`, 60자)를 저장                                     |
| `updated_at ... ON UPDATE` | UPDATE가 일어나면 **자동으로** 현재 시각으로 바뀜 → 비밀번호 수정 확인에 사용     |
| `utf8mb4`                  | 한글·이모지 저장                                                                  |

---

## 2. 핵심 개념

### 2-1. PyMySQL 기본 사용법

```python
import pymysql

conn = pymysql.connect(
    host="127.0.0.1", port=3306,
    user="root", password="1234",           # ← 본인 비밀번호
    database="fastapi_db", charset="utf8mb4",
    cursorclass=pymysql.cursors.DictCursor, # 결과를 dict로 받기
)

with conn:                                   # 블록이 끝나면 연결 자동 종료
    with conn.cursor() as cur:
        cur.execute("SELECT id, name FROM user WHERE id = %s", (1,))
        row = cur.fetchone()                 # {"id": 1, "name": "홍길동"} 또는 None
        print(row)
```

| 메서드                     | 의미                                      |
| -------------------------- | ----------------------------------------- |
| `conn.cursor()`            | SQL을 실행할 커서 생성                    |
| `cur.execute(sql, 값튜플)` | SQL 실행                                  |
| `cur.fetchone()`           | 결과 1행 (없으면 None)                    |
| `cur.fetchall()`           | 결과 전체 (리스트)                        |
| `cur.lastrowid`            | 방금 INSERT한 행의 AUTO_INCREMENT id      |
| `conn.commit()`            | **INSERT/UPDATE/DELETE를 DB에 확정 반영** |
| `conn.rollback()`          | 반영 전 작업 취소                         |

> ⚠️ **commit을 빼먹으면?** 에러 없이 실행되지만 **DB에 저장되지 않습니다.** (Workbench에서 SELECT 해 보면 비어 있음)

> ⚠️ **DictCursor를 빼면?** 결과가 `(1, '홍길동')` 같은 튜플로 나와서 `row["name"]`을 쓸 수 없습니다.

### 2-2. SQL 인젝션 방지 — 반드시 `%s`

```python
# ❌ 절대 금지: 문자열을 직접 이어 붙이기
cur.execute(f"SELECT * FROM user WHERE phone = '{phone}'")
#   phone에 ' OR '1'='1 을 넣으면 → 모든 회원이 조회됨 (SQL 인젝션)

# ✅ 올바른 방법: %s 자리표시자 + 값은 튜플로 따로 전달
cur.execute("SELECT * FROM user WHERE phone = %s", (phone,))
```

- `%s`는 문자열 포맷이 아니라 **PyMySQL이 값을 안전하게 처리해 주는 자리**입니다. 숫자여도 `%s`를 씁니다.
- 값이 1개일 때는 `(user_id,)`처럼 **쉼표**를 붙여야 튜플이 됩니다. `(user_id)`는 괄호만 있는 그냥 숫자입니다. (현재 PyMySQL 1.2는 동작은 하지만 "single argument is deprecated" 경고를 내며, 다음 버전에서 제거 예정)

### 2-3. 정규표현식으로 휴대폰 검증

```python
PHONE_PATTERN = r"^010-\d{4}-\d{4}$"
```

| 기호      | 의미                                       |
| --------- | ------------------------------------------ |
| `^` / `$` | 문자열의 시작 / 끝 (앞뒤로 다른 글자 금지) |
| `010-`    | 글자 그대로 "010-"                         |
| `\d{4}`   | 숫자 4개                                   |

| 입력            | 결과           |
| --------------- | -------------- |
| `010-1234-5678` | ✅             |
| `01012345678`   | ❌ 하이픈 없음 |
| `010-12-5678`   | ❌ 자릿수 부족 |
| `011-1234-5678` | ❌ 010 아님    |

Pydantic `Field(pattern=PHONE_PATTERN)`로 서버에서 검증하고, HTML `<input pattern="010-[0-9]{4}-[0-9]{4}">`로 브라우저에서도 한 번 더 막습니다.

> 💡 **브라우저 검증만으로는 부족합니다.** Postman이나 curl은 브라우저를 거치지 않으므로 **서버 검증이 필수**입니다.

### 2-4. bcrypt 비밀번호 해시

```python
import bcrypt

hashed = bcrypt.hashpw("pass1234".encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
print(hashed)        # $2b$12$Kx... (60자, 실행할 때마다 다름)

bcrypt.checkpw("pass1234".encode("utf-8"), hashed.encode("utf-8"))   # True
bcrypt.checkpw("wrong".encode("utf-8"), hashed.encode("utf-8"))      # False
```

- **해시**: 되돌릴 수 없는 변환. DB가 유출돼도 원래 비밀번호를 알 수 없음
- **salt**: `gensalt()`가 매번 무작위 값을 섞음 → 같은 비밀번호라도 해시가 매번 다름
- 그래서 로그인·본인 확인은 "다시 해시해서 비교"가 아니라 **`checkpw`로 비교**합니다.
- bcrypt는 `bytes`를 다루므로 `.encode("utf-8")` / `.decode("utf-8")`가 필요합니다.

> ⚠️ bcrypt는 비밀번호가 **72바이트를 넘으면 에러**가 납니다. 그래서 비밀번호를 최대 20자로 제한했습니다.

---

## 3. v1 — main.py 한 파일 + HTML 화면

### STEP 1. DB 접속 정보

```python
DB_CONFIG = {
    "host": "127.0.0.1",
    "port": 3306,
    "user": "root",
    "password": "1234",            # ← 본인 MySQL 비밀번호로 변경
    "database": "fastapi_db",
    "charset": "utf8mb4",
    "cursorclass": pymysql.cursors.DictCursor,
}


def get_connection():
    return pymysql.connect(**DB_CONFIG)
```

### STEP 2. DB·테이블 자동 생성 (lifespan)

```python
def init_db():
    # 1) database 없이 접속해서 DB 생성
    config = {k: v for k, v in DB_CONFIG.items() if k != "database"}
    with pymysql.connect(**config) as conn:
        with conn.cursor() as cur:
            cur.execute(
                f"CREATE DATABASE IF NOT EXISTS {DB_CONFIG['database']} "
                "DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"
            )
        conn.commit()

    # 2) 만든 DB에 접속해서 user 테이블 생성
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(CREATE_USER_TABLE)      # 1-3의 CREATE TABLE 문
        conn.commit()


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()      # 서버가 켜질 때 1번 실행
    yield


app = FastAPI(title="회원 관리 v1", lifespan=lifespan)
templates = Jinja2Templates(directory="templates")
```

> ✅ **중간 점검**: `uvicorn main:app --reload` 실행 → Workbench에서 `SHOW TABLES FROM fastapi_db;` → `user`가 보이면 성공

### STEP 3. bcrypt 함수

```python
def hash_password(plain: str) -> str:
    return bcrypt.hashpw(plain.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def verify_password(plain: str, hashed: str) -> bool:
    return bcrypt.checkpw(plain.encode("utf-8"), hashed.encode("utf-8"))
```

### STEP 4. Pydantic 모델

```python
PHONE_PATTERN = r"^010-\d{4}-\d{4}$"


class UserCreate(BaseModel):            # 회원가입 요청
    name: str = Field(..., min_length=1, max_length=50, examples=["홍길동"])
    phone: str = Field(..., pattern=PHONE_PATTERN, examples=["010-1234-5678"])
    password: str = Field(..., min_length=8, max_length=20, examples=["pass1234"])


class UserOut(BaseModel):               # 응답 (password 없음 → 자동으로 숨겨짐)
    id: int
    name: str
    phone: str
    created_at: datetime


class PasswordUpdate(BaseModel):        # 비밀번호 수정 요청
    current_password: str
    new_password: str = Field(..., min_length=8, max_length=20)


class UserDelete(BaseModel):            # 회원 탈퇴 요청 (본인 확인용)
    password: str
```

> 💡 `UserOut`에 password가 없으므로 `response_model=UserOut`을 쓰면 응답에서 **자동으로 빠집니다.** (5.6절 응답 모델)

### STEP 5. DB 함수 (SQL 직접 작성)

```python
def db_create_user(name: str, phone: str, hashed_pw: str) -> int:
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO user (name, phone, password) VALUES (%s, %s, %s)",
                (name, phone, hashed_pw),
            )
            new_id = cur.lastrowid       # 방금 생성된 id
        conn.commit()
    return new_id


def db_get_users() -> list:
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT id, name, phone, created_at FROM user ORDER BY id DESC")
            return cur.fetchall()


def db_get_user(user_id: int):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT id, name, phone, created_at FROM user WHERE id = %s", (user_id,))
            return cur.fetchone()


def db_get_password_hash(user_id: int):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT password FROM user WHERE id = %s", (user_id,))
            row = cur.fetchone()
            return row["password"] if row else None


def db_update_password(user_id: int, hashed_pw: str) -> None:
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("UPDATE user SET password = %s WHERE id = %s", (hashed_pw, user_id))
        conn.commit()


def db_delete_user(user_id: int) -> None:
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM user WHERE id = %s", (user_id,))
        conn.commit()
```

> 💡 조회 SQL에서 `SELECT *`가 아니라 **password를 뺀 컬럼만** 조회합니다. 비밀번호 해시는 본인 확인 함수(`db_get_password_hash`)에서만 꺼냅니다.

### STEP 6. 업무 로직 (API와 HTML이 함께 사용)

```python
def signup(data: UserCreate) -> int:
    try:
        return db_create_user(data.name, data.phone, hash_password(data.password))
    except pymysql.err.IntegrityError:       # phone UNIQUE 위반 = 중복 가입
        raise HTTPException(status_code=409, detail="이미 가입된 휴대폰 번호입니다.")


def check_password(user_id: int, password: str) -> None:
    hashed = db_get_password_hash(user_id)
    if hashed is None:
        raise HTTPException(status_code=404, detail="회원을 찾을 수 없습니다.")
    if not verify_password(password, hashed):
        raise HTTPException(status_code=401, detail="비밀번호가 일치하지 않습니다.")


def change_password(user_id: int, current_pw: str, new_pw: str) -> None:
    check_password(user_id, current_pw)
    if current_pw == new_pw:
        raise HTTPException(status_code=400, detail="새 비밀번호가 현재 비밀번호와 같습니다.")
    db_update_password(user_id, hash_password(new_pw))


def withdraw(user_id: int, password: str) -> None:
    check_password(user_id, password)
    db_delete_user(user_id)
```

> 💡 **중복 확인을 SELECT로 먼저 하지 않는 이유**: 두 사람이 동시에 같은 번호로 가입하면 SELECT 확인을 둘 다 통과할 수 있습니다. DB의 UNIQUE 제약이 최종적으로 막아 주므로 **IntegrityError를 잡는 방식**이 더 안전합니다.

### STEP 7. JSON API (Postman 테스트 대상)

```python
@app.post("/api/users", response_model=UserOut, status_code=201)
def api_signup(user: UserCreate):
    new_id = signup(user)
    return db_get_user(new_id)


@app.get("/api/users", response_model=List[UserOut])
def api_get_users():
    return db_get_users()


@app.get("/api/users/{user_id}", response_model=UserOut)
def api_get_user(user_id: int):
    user = db_get_user(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="회원을 찾을 수 없습니다.")
    return user


@app.put("/api/users/{user_id}/password")
def api_change_password(user_id: int, body: PasswordUpdate):
    change_password(user_id, body.current_password, body.new_password)
    return {"message": "비밀번호가 변경되었습니다."}


@app.delete("/api/users/{user_id}")
def api_withdraw(user_id: int, body: UserDelete):
    withdraw(user_id, body.password)
    return {"message": "회원 탈퇴가 완료되었습니다."}
```

> ✅ **중간 점검**:

### STEP 8. HTML 화면

**핵심 패턴 3가지**

1. **폼 데이터 받기** — `Form(...)`. HTML `<input name="phone">`의 name = 함수 매개변수 이름
2. **검증 재사용** — `UserCreate(name=..., phone=..., password=...)`를 만들면 Pydantic 검증이 실행됨 → `ValidationError`를 잡아 한글 메시지로 표시
3. **PRG 패턴** — 처리 성공 후 `RedirectResponse(주소, status_code=303)`. POST 후 GET 화면으로 이동하므로 **새로고침해도 중복 가입되지 않음**

```python
@app.post("/signup")
def page_signup(
    request: Request,
    name: str = Form(...),
    phone: str = Form(...),
    password: str = Form(...),
):
    form = {"name": name, "phone": phone}       # 에러 시 입력값 유지 (비밀번호 제외)
    try:
        signup(UserCreate(name=name, phone=phone, password=password))
    except ValidationError as e:                 # 형식 오류 → 한글 메시지
        return templates.TemplateResponse(
            request, "signup.html", {"error": validation_message(e), "form": form}, status_code=400
        )
    except HTTPException as e:                   # 중복 가입 409
        return templates.TemplateResponse(
            request, "signup.html", {"error": e.detail, "form": form}, status_code=e.status_code
        )
    return RedirectResponse("/?msg=signup", status_code=303)
```

나머지 화면(목록, 상세, 비밀번호 수정, 탈퇴)도 같은 패턴입니다. 전체 코드는 `instructor/v1/main.py` STEP 8을 참고하세요.

**템플릿 구조** (`templates/`)

| 파일          | 내용                                           | 받는 값          |
| ------------- | ---------------------------------------------- | ---------------- |
| `base.html`   | 공통 레이아웃, 메뉴, 성공/에러 메시지 박스     | msg, error       |
| `index.html`  | 회원 목록 표 (이름 클릭 → 상세)                | users, msg       |
| `signup.html` | 가입 폼 (`pattern`, `minlength` 브라우저 검증) | error, form      |
| `detail.html` | 회원 정보 + 비밀번호 수정 폼 + 탈퇴 폼(확인창) | user, msg, error |

**브라우저 테스트 순서** — http://127.0.0.1:8000/

| 순서 | 동작                                          | 기대 결과                                      |
| ---- | --------------------------------------------- | ---------------------------------------------- |
| 1    | 회원가입 → 이영희 / 010-5555-6666 / hello1234 | 목록으로 이동 + "회원가입이 완료되었습니다."   |
| 2    | 같은 번호로 다시 가입                         | "이미 가입된 휴대폰 번호입니다." (입력값 유지) |
| 3    | 목록에서 이름 클릭                            | 회원 정보 화면                                 |
| 4    | 현재 비밀번호 틀리게 입력 후 변경             | "비밀번호가 일치하지 않습니다."                |
| 5    | 새 비밀번호 5자 입력                          | 브라우저가 막음 (minlength)                    |
| 6    | 올바르게 변경 (hello1234 → newhello99)        | "비밀번호가 변경되었습니다."                   |
| 7    | 탈퇴 — 예전 비밀번호(hello1234) 입력          | "비밀번호가 일치하지 않습니다."                |
| 8    | 탈퇴 — newhello99 입력 → 확인창 OK            | 목록으로 이동 + "회원 탈퇴가 완료되었습니다."  |

> 💡 F12 → Network 탭에서 가입 버튼을 누르면 `POST /signup` → **303** → `GET /?msg=signup` 순서로 요청이 이어지는 것을 볼 수 있습니다.

---

## 4. Postman으로 API 테스트

### 4-1. 컬렉션 가져오기 (추천)

1. Postman 실행 → 왼쪽 위 **Import** 클릭
2. `postman/회원관리_API.postman_collection.json` 파일을 끌어다 놓기
3. 왼쪽 Collections에 **"회원관리 API (FastAPI + MySQL)"** 가 생김
4. 서버 실행(`uvicorn main:app --reload`) 후 요청을 **1 → 5 순서대로** Send

> 💡 **1. 회원가입**이 성공(201)하면 응답의 `id`가 컬렉션 변수 `userId`에 **자동 저장**됩니다(Tests 탭 스크립트). 이후 요청 주소의 `{{userId}}`에 그 값이 들어갑니다.
> 확인: 컬렉션 이름 클릭 → **Variables** 탭

> 💡 컬렉션 이름 옆 `...` → **Run collection**을 누르면 1~5번을 한 번에 실행하고 결과를 보여 줍니다.

### 4-2. 직접 요청 만들기

**New → HTTP Request** 후 아래처럼 설정합니다.

| 설정 위치       | 값                                                                        |
| --------------- | ------------------------------------------------------------------------- |
| 메서드 드롭다운 | POST / GET / PUT / DELETE                                                 |
| 주소            | `http://127.0.0.1:8000/api/users`                                         |
| **Body** 탭     | **raw** 선택 → 오른쪽 드롭다운 **JSON** (Content-Type 헤더가 자동 추가됨) |
| 결과 확인       | 아래 Response 영역의 **Status**(201, 200, 422...)와 Body                  |

**① 회원가입** — `POST /api/users`

```json
{
  "name": "홍길동",
  "phone": "010-1234-5678",
  "password": "pass1234"
}
```

```json
201 Created
{"id": 1, "name": "홍길동", "phone": "010-1234-5678", "created_at": "2026-11-27T09:47:24"}
```

> password가 응답에 없는 것을 확인하세요. (response_model=UserOut)

**② 회원 목록** — `GET /api/users` (Body 없음)

```json
200 OK
[{"id": 1, "name": "홍길동", "phone": "010-1234-5678", "created_at": "2026-11-27T09:47:24"}]
```

**③ 회원 상세** — `GET /api/users/1`

```json
200 OK
{"id": 1, "name": "홍길동", "phone": "010-1234-5678", "created_at": "2026-11-27T09:47:24"}
```

**④ 비밀번호 수정** — `PUT /api/users/1/password`

```json
{
  "current_password": "pass1234",
  "new_password": "newpass99"
}
```

```json
200 OK
{"message": "비밀번호가 변경되었습니다."}
```

**⑤ 회원 탈퇴** — `DELETE /api/users/1`

```json
{
  "password": "newpass99"
}
```

```json
200 OK
{"message": "회원 탈퇴가 완료되었습니다."}
```

> 💡 DELETE 요청도 Body 탭에서 raw/JSON으로 바디를 보낼 수 있습니다.

### 4-3. 에러 케이스 확인

| 요청                | 보낸 값                     | 상태    | 응답                                                                            |
| ------------------- | --------------------------- | ------- | ------------------------------------------------------------------------------- |
| POST /api/users     | 이미 있는 phone             | **409** | `{"detail": "이미 가입된 휴대폰 번호입니다."}`                                  |
| POST /api/users     | phone `"01012345678"`       | **422** | `"loc": ["body","phone"], "type": "string_pattern_mismatch"`                    |
| POST /api/users     | password `"123"`            | **422** | `"loc": ["body","password"], "msg": "String should have at least 8 characters"` |
| GET /api/users/99   | 없는 번호                   | **404** | `{"detail": "회원을 찾을 수 없습니다."}`                                        |
| PUT .../password    | current_password 틀림       | **401** | `{"detail": "비밀번호가 일치하지 않습니다."}`                                   |
| PUT .../password    | 새 비밀번호 = 현재 비밀번호 | **400** | `{"detail": "새 비밀번호가 현재 비밀번호와 같습니다."}`                         |
| PUT .../password    | new_password `"short"`      | **422** | `"loc": ["body","new_password"]`                                                |
| DELETE /api/users/1 | password 틀림               | **401** | `{"detail": "비밀번호가 일치하지 않습니다."}`                                   |
| DELETE /api/users/1 | 이미 탈퇴한 회원            | **404** | `{"detail": "회원을 찾을 수 없습니다."}`                                        |

---

## 5. MySQL에서 데이터 확인하기

Postman/화면에서 요청을 보낼 때마다 Workbench에서 SQL로 **실제 DB가 바뀌었는지** 확인합니다. (`sql/schema.sql` 아래쪽에 확인용 SQL이 있습니다.)

| 시점              | 확인 SQL                                                              | 확인할 것                                                 |
| ----------------- | --------------------------------------------------------------------- | --------------------------------------------------------- |
| 가입 후           | `SELECT * FROM user;`                                                 | 새 행 추가, password가 `$2b$12$...` 해시인지              |
| 비밀번호 수정 후  | `SELECT id, password, created_at, updated_at FROM user WHERE id = 1;` | password 해시가 바뀜, **updated_at만** 현재 시각으로 바뀜 |
| 탈퇴 후           | `SELECT COUNT(*) FROM user WHERE id = 1;`                             | 0                                                         |
| 중복 가입 시도 후 | `SELECT * FROM user;`                                                 | 행이 늘지 않음                                            |

**실제 확인 결과 예 (비밀번호 수정 후)**

```
id  name    phone          password(앞 20자)        created_at           updated_at
1   홍길동  010-1234-5678  $2b$12$sFVIFcQvb1Ef8...   2026-11-27 09:47:24  2026-11-27 09:47:25
```

> 💡 **AUTO_INCREMENT 번호가 건너뛰는 이유**: 중복 가입처럼 INSERT가 실패해도 번호는 이미 사용된 것으로 처리됩니다. 그래서 다음 가입자는 3번이 아니라 4번이 될 수 있습니다. 정상 동작입니다.

> ⚠️ Workbench에서 SELECT 결과가 안 바뀌면 결과창 위의 **새로고침(⚡ 다시 실행)** 을 누르세요.

---

## 6. v2 — 실무형 프로젝트 구조로 나누기

> 학생 실습용: `student/v2/` (①~⑧ 파일 순서대로, 마지막에 main.py)

### 6-1. 왜 나누나?

v1은 한 파일에 설정, DB, 검증, SQL, API, 화면이 모두 섞여 있어 300줄이 넘습니다. 기능이 늘면 찾기도 고치기도 어려워집니다. **역할별로 파일을 나누면** 수정할 곳이 명확해지고 여러 사람이 동시에 작업하기 쉬워집니다.

### 6-2. 폴더 구조와 역할

```
v2/
├── main.py                 ← 앱 생성 + lifespan + 라우터 등록
├── app/
│   ├── __init__.py         ← app 폴더를 패키지로 인식 (빈 파일)
│   ├── config.py           ← DB 접속 정보 (환경변수 지원)
│   ├── database.py         ← get_connection, get_db(의존성), init_db
│   ├── schemas.py          ← Pydantic 모델
│   ├── security.py         ← bcrypt
│   ├── crud.py             ← SQL만 (conn을 매개변수로 받음)
│   ├── services.py         ← 업무 규칙 (중복·본인 확인 → HTTPException)
│   └── routers/
│       ├── __init__.py
│       ├── api_users.py    ← JSON API (prefix="/api/users")
│       └── pages.py        ← HTML 화면
└── templates/              ← v1과 동일
```

| v1 STEP             | v2 파일                              |
| ------------------- | ------------------------------------ |
| STEP 1 DB 접속 정보 | `config.py` + `database.py`          |
| STEP 2 테이블 생성  | `database.py` + `main.py` (lifespan) |
| STEP 3 bcrypt       | `security.py`                        |
| STEP 4 Pydantic     | `schemas.py`                         |
| STEP 5 DB 함수      | `crud.py`                            |
| STEP 6 업무 로직    | `services.py`                        |
| STEP 7 JSON API     | `routers/api_users.py`               |
| STEP 8 HTML 화면    | `routers/pages.py`                   |

### 6-3. v1과 달라지는 핵심 3가지

**① 설정 분리 — config.py**

```python
import os

DB_HOST = os.getenv("DB_HOST", "127.0.0.1")
DB_PORT = int(os.getenv("DB_PORT", "3306"))
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "1234")    # ← 본인 MySQL 비밀번호
DB_NAME = os.getenv("DB_NAME", "fastapi_db")
```

비밀번호를 코드에 직접 쓰지 않고 환경변수로 바꿀 수 있습니다. (PowerShell: `$env:DB_PASSWORD="mypassword"`)

**② 의존성 주입 — get_db + Depends**

```python
# database.py
def get_db():
    conn = get_connection()
    try:
        yield conn          # 라우터 함수에 연결을 넘겨줌
    finally:
        conn.close()        # 응답이 끝나면 반드시 닫힘 (에러가 나도)
```

```python
# routers/api_users.py
@router.get("", response_model=List[UserOut], summary="회원 목록 조회")
def api_get_users(conn=Depends(get_db)):
    return crud.get_users(conn)
```

```python
# crud.py — 연결을 받아서 쓰기만 함 (열고 닫지 않음)
def get_users(conn) -> list:
    with conn.cursor() as cur:
        cur.execute("SELECT id, name, phone, created_at FROM user ORDER BY id DESC")
        return cur.fetchall()
```

> 💡 v1은 DB 함수마다 연결을 새로 열고 닫았습니다. v2는 **요청 1번에 연결 1개**를 열어 여러 함수가 함께 쓰고, 응답이 끝나면 FastAPI가 닫아 줍니다.

**③ APIRouter — 경로를 파일별로 나누기**

```python
# routers/api_users.py
router = APIRouter(prefix="/api/users", tags=["회원 API"])

@router.post("", response_model=UserOut, status_code=201, summary="회원가입")
def api_signup(user: UserCreate, conn=Depends(get_db)):
    new_id = services.signup(conn, user)
    return crud.get_user(conn, new_id)
```

```python
# main.py
app.include_router(api_users.router)    # /api/users ...
app.include_router(pages.router)        # /, /signup, /users/...
```

- `prefix`: 모든 경로 앞에 자동으로 붙음 (`@router.post("")` → `POST /api/users`)
- `tags`: `/docs`에서 "회원 API" 그룹으로 묶여 보임
- `pages.py`의 `APIRouter(include_in_schema=False)`: 화면용 경로는 `/docs`에 표시하지 않음

### 6-4. 실행과 검증

```bash
cd v2
uvicorn main:app --reload
```

> ⚠️ 반드시 **v2 폴더(main.py가 있는 곳)** 에서 실행하세요. 다른 위치에서 실행하면 `ModuleNotFoundError: No module named 'app'` 또는 템플릿을 찾지 못하는 에러가 납니다.

v1과 **같은 Postman 컬렉션, 같은 브라우저 테스트**로 결과가 완전히 같아야 합니다. (실제 검증 시 v1·v2 결과 동일 확인)

---

## 7. 자주 나는 에러

| 에러 메시지                                                                                    | 원인                          | 해결                                     |
| ---------------------------------------------------------------------------------------------- | ----------------------------- | ---------------------------------------- |
| `(1045, "Access denied for user 'root'@'localhost'")`                                          | DB 비밀번호 틀림              | DB_CONFIG / config.py의 password 확인    |
| `(2003, "Can't connect to MySQL server on '127.0.0.1'")`                                       | MySQL 서버가 꺼져 있음        | Windows 서비스에서 MySQL80 시작          |
| `'cryptography' package is required for sha256_password or caching_sha2_password auth methods` | MySQL 8 인증 방식             | `pip install cryptography`               |
| `(1049, "Unknown database 'fastapi_db'")`                                                      | DB 없음                       | init_db() 실행 확인 또는 schema.sql 실행 |
| `Form data requires "python-multipart" to be installed`                                        | HTML 폼 처리 패키지 없음      | `pip install python-multipart`           |
| `TemplateNotFound: index.html`                                                                 | templates 폴더 위치           | main.py가 있는 폴더에서 서버 실행        |
| `ModuleNotFoundError: No module named 'app'` (v2)                                              | 실행 위치                     | v2 폴더에서 실행                         |
| 가입은 성공인데 DB에 데이터가 없음                                                             | `commit()` 누락               | INSERT 후 `conn.commit()`                |
| `TypeError: tuple indices must be integers or slices, not str`                                 | DictCursor 누락 (결과가 튜플) | `cursorclass=pymysql.cursors.DictCursor` |
| `DeprecationWarning: single argument is deprecated`                                            | 값 튜플 쉼표 누락 `(user_id)` | `(user_id,)`                             |
| `ValueError: password cannot be longer than 72 bytes`                                          | bcrypt 길이 제한              | 비밀번호 max_length 20 유지              |

---

## 8. 정리

| 개념                   | 핵심                                                                       |
| ---------------------- | -------------------------------------------------------------------------- |
| PyMySQL                | `connect` → `cursor` → `execute(sql, 값)` → `fetchone/fetchall` → `commit` |
| SQL 인젝션 방지        | 값은 항상 `%s` + 튜플                                                      |
| 정규표현식             | `^010-\d{4}-\d{4}$` / 서버(Pydantic) + 브라우저(pattern) 이중 검증         |
| bcrypt                 | `hashpw`로 저장, `checkpw`로 비교 / 평문 저장 금지                         |
| 응답에서 비밀번호 숨김 | `response_model=UserOut` (password 필드 없음)                              |
| 중복 가입              | DB UNIQUE + IntegrityError → 409                                           |
| 본인 확인              | 수정·탈퇴 전 비밀번호 확인 → 401                                           |
| HTML 폼                | GET/POST만 가능 → 수정·삭제도 POST, 처리 후 303 리디렉션(PRG)              |
| v2 구조                | config / database(get_db) / schemas / security / crud / services / routers |

---

## 9. 실습 과제

1. **이름 수정 기능**: `PUT /api/users/{user_id}/name` (바디: password, new_name)과 상세 화면의 이름 수정 폼을 추가하세요. 수정 후 Workbench에서 `updated_at`이 바뀌는지 확인하세요.
2. **휴대폰 번호 가리기**: 회원 목록 화면에서 휴대폰 번호를 `010-****-5678`처럼 가려서 보여 주세요. (힌트: Jinja2에서 `user.phone[:4] ~ '****' ~ user.phone[8:]`)
3. **휴대폰으로 회원 찾기**: `GET /api/users/search?phone=010-1234-5678` 를 만들고, phone 쿼리 매개변수에 `Query(..., pattern=...)`로 형식 검증을 넣으세요. (주의: `/api/users/{user_id}`보다 **위에** 선언해야 합니다. 이유는?)
4. **로그인 확인 API**: `POST /api/login` (바디: phone, password) → 일치하면 `{"message": "로그인 성공", "user_id": ...}`, 아니면 401을 반환하세요.
5. (도전) **v2에 1~4번 기능 추가**: 어떤 파일에 어떤 코드를 넣어야 하는지 먼저 표로 정리한 뒤 구현하세요.
