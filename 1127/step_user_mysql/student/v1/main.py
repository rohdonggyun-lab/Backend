# =====================================================================
#  회원 관리 v1 (학생용 템플릿) — main.py 한 파일 + HTML 템플릿
# =====================================================================
#  🎯 목표: 회원가입 / 회원 조회 / 비밀번호 수정 / 회원 탈퇴
#           - DB  : MySQL + PyMySQL (SQLAlchemy 사용 X → SQL 직접 작성)
#           - 보안 : 비밀번호는 bcrypt 해시로 저장
#           - 화면 : templates/ 폴더의 HTML (완성본 제공 — 수정 불필요)
#           - API : /api/users (Postman으로 테스트)
#
#  📁 폴더 구조
#    v1/
#    ├── main.py              ← 지금 이 파일 (TODO를 채워 완성)
#    ├── requirements.txt
#    └── templates/           ← 완성본 (base / index / signup / detail)
#
#  📚 작업 순서 (위에서 아래로, STEP 번호 순서대로!)
#    STEP 0. 준비      : pip install -r requirements.txt / MySQL 서버 실행 확인
#    STEP 1. DB 접속 정보 작성 → get_connection()
#    STEP 2. 테이블 생성 SQL 작성 → init_db() → 서버 실행해서 테이블 생성 확인
#    STEP 3. bcrypt 함수 2개 작성
#    STEP 4. Pydantic 모델 4개 작성
#    STEP 5. DB 함수 6개 작성 (SQL)
#    STEP 6. 업무 로직 함수 4개 작성
#    STEP 7. JSON API 5개 작성 → Postman 테스트 + MySQL에서 데이터 확인
#    STEP 8. HTML 화면 6개 작성 → 브라우저 테스트
#
#  ✅ 중간 점검 방법
#    - STEP 2 후 : uvicorn main:app --reload 실행 → Workbench에서 SHOW TABLES;
#    - STEP 7 후 : Postman으로 /api/users 테스트 → SELECT * FROM user;
#    - STEP 8 후 : http://127.0.0.1:8000/ 에서 가입 → 상세 → 수정 → 탈퇴
#
#  ▶ 실행 : uvicorn main:app --reload
# =====================================================================

from contextlib import asynccontextmanager
from datetime import datetime
from typing import List

import bcrypt
import pymysql
from fastapi import FastAPI, Form, HTTPException, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field, ValidationError


# ---------------------------------------------------------------------
# STEP 1. DB 접속 정보
# ---------------------------------------------------------------------
# TODO 1-1: 아래 딕셔너리에 접속 정보를 채우세요.
#   host        : "127.0.0.1"
#   port        : 3306
#   user        : "root"
#   password    : 본인 MySQL 비밀번호
#   database    : "fastapi_db"
#   charset     : "utf8mb4"                          (한글·이모지 저장)
#   cursorclass : pymysql.cursors.DictCursor        (결과를 dict로 받기)
DB_CONFIG = {
    # 여기에 작성
}


def get_connection():
    # TODO 1-2: pymysql.connect(**DB_CONFIG) 를 반환하세요.
    #   ** 는 딕셔너리를 키=값 인자로 풀어서 전달하는 문법입니다.
    pass


# ---------------------------------------------------------------------
# STEP 2. DB와 user 테이블 만들기 (서버 시작 시 자동 실행)
# ---------------------------------------------------------------------
# TODO 2-1: user 테이블 생성 SQL을 완성하세요. (CREATE TABLE IF NOT EXISTS user (...))
#   컬럼        타입            조건
#   id          INT             AUTO_INCREMENT PRIMARY KEY
#   name        VARCHAR(50)     NOT NULL
#   phone       VARCHAR(13)     NOT NULL UNIQUE       ← 중복 가입 방지
#   password    VARCHAR(255)    NOT NULL              ← bcrypt 해시 저장
#   created_at  DATETIME        DEFAULT CURRENT_TIMESTAMP
#   updated_at  DATETIME        DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
CREATE_USER_TABLE = """
"""


def init_db():
    # TODO 2-2: DB 생성
    #   ① DB_CONFIG에서 "database"만 뺀 설정 만들기
    #        config = {k: v for k, v in DB_CONFIG.items() if k != "database"}
    #   ② with pymysql.connect(**config) as conn:
    #          with conn.cursor() as cur:
    #              cur.execute("CREATE DATABASE IF NOT EXISTS fastapi_db "
    #                          "DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
    #          conn.commit()
    #
    # TODO 2-3: 테이블 생성
    #   ③ with get_connection() as conn: → cursor로 CREATE_USER_TABLE 실행 → commit
    pass


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()      # 서버가 켜질 때 1번 실행
    yield


app = FastAPI(title="회원 관리 v1", lifespan=lifespan)
templates = Jinja2Templates(directory="templates")


# ---------------------------------------------------------------------
# STEP 3. 비밀번호 암호화 (bcrypt)
# ---------------------------------------------------------------------
def hash_password(plain: str) -> str:
    # TODO 3-1: 평문 → 해시 문자열
    #   bcrypt는 bytes를 다룹니다 → 문자열.encode("utf-8") 로 변환
    #   bcrypt.hashpw(비밀번호bytes, bcrypt.gensalt()) → 결과 bytes를 .decode("utf-8")
    pass


def verify_password(plain: str, hashed: str) -> bool:
    # TODO 3-2: 평문과 해시 비교
    #   bcrypt.checkpw(평문bytes, 해시bytes) → True / False
    pass


# ---------------------------------------------------------------------
# STEP 4. Pydantic 모델 (요청 검증 / 응답 형식)
# ---------------------------------------------------------------------
PHONE_PATTERN = r"^010-\d{4}-\d{4}$"   # 010-1234-5678 형식만 허용


class UserCreate(BaseModel):
    # TODO 4-1: 회원가입 요청 모델
    #   name     : str, 필수, 1~50자          Field(..., min_length=1, max_length=50)
    #   phone    : str, 필수, PHONE_PATTERN    Field(..., pattern=PHONE_PATTERN)
    #   password : str, 필수, 8~20자
    pass


class UserOut(BaseModel):
    # TODO 4-2: 응답 모델 — id(int), name(str), phone(str), created_at(datetime)
    #   ※ password는 넣지 않습니다! → response_model로 쓰면 응답에서 자동으로 빠짐
    pass


class PasswordUpdate(BaseModel):
    # TODO 4-3: current_password(str), new_password(str, 8~20자)
    pass


class UserDelete(BaseModel):
    # TODO 4-4: password(str)  ← 탈퇴 전 본인 확인용
    pass


# ---------------------------------------------------------------------
# STEP 5. DB 함수 (SQL 직접 작성)
# ---------------------------------------------------------------------
#  📌 공통 패턴
#    with get_connection() as conn:          ← 블록이 끝나면 연결 자동 종료
#        with conn.cursor() as cur:
#            cur.execute("SQL ... %s", (값,))  ← 값은 반드시 %s 로! (SQL 인젝션 방지)
#            결과 = cur.fetchone() / cur.fetchall()
#        conn.commit()                       ← INSERT/UPDATE/DELETE만 필요
#
#  ⚠️ 값이 1개일 때 튜플은 (user_id,) 처럼 쉼표 필수!
# ---------------------------------------------------------------------
def db_create_user(name: str, phone: str, hashed_pw: str) -> int:
    # TODO 5-1: INSERT INTO user (name, phone, password) VALUES (%s, %s, %s)
    #   실행 후 cur.lastrowid(새 회원 id)를 저장 → commit → id 반환
    pass


def db_get_users() -> list:
    # TODO 5-2: SELECT id, name, phone, created_at FROM user ORDER BY id DESC
    #   cur.fetchall() 반환   (password 컬럼은 조회하지 않기!)
    pass


def db_get_user(user_id: int):
    # TODO 5-3: SELECT id, name, phone, created_at FROM user WHERE id = %s
    #   cur.fetchone() 반환   (없으면 None)
    pass


def db_get_password_hash(user_id: int):
    # TODO 5-4: SELECT password FROM user WHERE id = %s
    #   row = cur.fetchone() → row가 있으면 row["password"], 없으면 None 반환
    pass


def db_update_password(user_id: int, hashed_pw: str) -> None:
    # TODO 5-5: UPDATE user SET password = %s WHERE id = %s → commit
    pass


def db_delete_user(user_id: int) -> None:
    # TODO 5-6: DELETE FROM user WHERE id = %s → commit
    pass


# ---------------------------------------------------------------------
# STEP 6. 업무 로직 (API와 HTML 화면이 함께 사용)
#   문제가 있으면 raise HTTPException(status_code=..., detail="...")
# ---------------------------------------------------------------------
def signup(data: UserCreate) -> int:
    # TODO 6-1: 회원가입
    #   try:
    #       data.password를 hash_password()로 해시 → db_create_user() 호출 → id 반환
    #   except pymysql.err.IntegrityError:      ← phone UNIQUE 위반 = 중복 가입
    #       409, "이미 가입된 휴대폰 번호입니다."
    pass


def check_password(user_id: int, password: str) -> None:
    # TODO 6-2: 본인 확인
    #   ① hashed = db_get_password_hash(user_id)
    #   ② hashed가 None    → 404, "회원을 찾을 수 없습니다."
    #   ③ verify_password 실패 → 401, "비밀번호가 일치하지 않습니다."
    pass


def change_password(user_id: int, current_pw: str, new_pw: str) -> None:
    # TODO 6-3: 비밀번호 변경
    #   ① check_password(user_id, current_pw)
    #   ② current_pw == new_pw → 400, "새 비밀번호가 현재 비밀번호와 같습니다."
    #   ③ db_update_password(user_id, hash_password(new_pw))
    pass


def withdraw(user_id: int, password: str) -> None:
    # TODO 6-4: 회원 탈퇴 — check_password() → db_delete_user()
    pass


# =====================================================================
# STEP 7. JSON API (Postman으로 테스트)
# =====================================================================
#  | 기능        | 메서드 | 주소                          | 요청 바디          | 성공 응답
#  | 회원가입    | POST   | /api/users                    | UserCreate         | 201 + UserOut
#  | 목록 조회   | GET    | /api/users                    | -                  | 200 + List[UserOut]
#  | 상세 조회   | GET    | /api/users/{user_id}          | -                  | 200 + UserOut (없으면 404)
#  | 비번 수정   | PUT    | /api/users/{user_id}/password | PasswordUpdate     | 200 + {"message": ...}
#  | 회원 탈퇴   | DELETE | /api/users/{user_id}          | UserDelete         | 200 + {"message": ...}
# =====================================================================
@app.post("/api/users", response_model=UserOut, status_code=201)
def api_signup(user: UserCreate):
    # TODO 7-1: new_id = signup(user) → db_get_user(new_id) 반환
    pass


@app.get("/api/users", response_model=List[UserOut])
def api_get_users():
    # TODO 7-2: db_get_users() 반환
    pass


@app.get("/api/users/{user_id}", response_model=UserOut)
def api_get_user(user_id: int):
    # TODO 7-3: db_get_user(user_id) → None이면 404 "회원을 찾을 수 없습니다." → 아니면 반환
    pass


@app.put("/api/users/{user_id}/password")
def api_change_password(user_id: int, body: PasswordUpdate):
    # TODO 7-4: change_password(...) 호출 → {"message": "비밀번호가 변경되었습니다."}
    pass


@app.delete("/api/users/{user_id}")
def api_withdraw(user_id: int, body: UserDelete):
    # TODO 7-5: withdraw(...) 호출 → {"message": "회원 탈퇴가 완료되었습니다."}
    pass


# =====================================================================
# STEP 8. HTML 화면
# =====================================================================
#  📌 HTML <form>은 GET/POST만 보낼 수 있습니다.
#     → 비밀번호 수정·탈퇴도 POST + 별도 주소(/password, /delete)로 받습니다.
#  📌 폼 데이터는 Form(...)으로 받습니다. (python-multipart 설치 필요)
#     input의 name 속성 = 함수 매개변수 이름
#  📌 처리 성공 후에는 RedirectResponse(주소, status_code=303)
#     → POST 후 GET으로 이동 (새로고침해도 중복 전송 안 됨, PRG 패턴)
#  📌 템플릿에 넘기는 값
#     index.html  : users(목록), msg
#     signup.html : error, form({"name":..., "phone":...} 입력값 유지용)
#     detail.html : user, msg, error
# =====================================================================
MESSAGES = {
    "signup": "회원가입이 완료되었습니다.",
    "deleted": "회원 탈퇴가 완료되었습니다.",
    "password": "비밀번호가 변경되었습니다.",
}

FIELD_ERRORS = {
    "name": "이름은 1~50자로 입력하세요.",
    "phone": "휴대폰 번호는 010-1234-5678 형식으로 입력하세요.",
    "password": "비밀번호는 8~20자로 입력하세요.",
    "new_password": "새 비밀번호는 8~20자로 입력하세요.",
}


def validation_message(e: ValidationError) -> str:
    """Pydantic 검증 에러 → 화면에 보여줄 한글 메시지 (완성본 제공)"""
    field = e.errors()[0]["loc"][0]
    return FIELD_ERRORS.get(field, "입력값을 확인하세요.")


@app.get("/")
def page_index(request: Request, msg: str = ""):
    # TODO 8-1: 회원 목록 화면
    #   templates.TemplateResponse(request, "index.html",
    #       {"users": db_get_users(), "msg": MESSAGES.get(msg, "")})
    pass


@app.get("/signup")
def page_signup_form(request: Request):
    # TODO 8-2: 회원가입 폼 화면 — signup.html, {"error": "", "form": {}}
    pass


@app.post("/signup")
def page_signup(
    request: Request,
    name: str = Form(...),
    phone: str = Form(...),
    password: str = Form(...),
):
    # TODO 8-3: 회원가입 처리
    #   ① form = {"name": name, "phone": phone}        ← 에러 시 입력값 유지 (비밀번호 제외)
    #   ② try: signup(UserCreate(name=..., phone=..., password=...))
    #        ※ UserCreate(...)를 만들 때 Pydantic 검증이 실행됩니다.
    #   ③ except ValidationError as e:
    #        signup.html 다시 보여주기, error=validation_message(e), status_code=400
    #   ④ except HTTPException as e:   (중복 가입 409)
    #        signup.html 다시 보여주기, error=e.detail, status_code=e.status_code
    #   ⑤ 성공: RedirectResponse("/?msg=signup", status_code=303)
    pass


def render_detail(request: Request, user_id: int, msg: str = "", error: str = "", status_code: int = 200):
    # TODO 8-4: 회원 상세 화면 공통 함수
    #   ① user = db_get_user(user_id) → None이면 404 HTTPException
    #   ② detail.html, {"user": user, "msg": msg, "error": error}, status_code=status_code
    pass


@app.get("/users/{user_id}")
def page_detail(request: Request, user_id: int, msg: str = ""):
    # TODO 8-5: render_detail(request, user_id, msg=MESSAGES.get(msg, "")) 반환
    pass


@app.post("/users/{user_id}/password")
def page_change_password(
    request: Request,
    user_id: int,
    current_password: str = Form(...),
    new_password: str = Form(...),
):
    # TODO 8-6: 비밀번호 수정 처리
    #   ① try: body = PasswordUpdate(...) → change_password(user_id, ...)
    #   ② except ValidationError → render_detail(..., error=validation_message(e), status_code=400)
    #   ③ except HTTPException as e:
    #        404면 그대로 raise / 아니면 render_detail(..., error=e.detail, status_code=e.status_code)
    #   ④ 성공: RedirectResponse(f"/users/{user_id}?msg=password", status_code=303)
    pass


@app.post("/users/{user_id}/delete")
def page_withdraw(request: Request, user_id: int, password: str = Form(...)):
    # TODO 8-7: 회원 탈퇴 처리
    #   ① try: withdraw(user_id, password)
    #   ② except HTTPException → 8-6의 ③과 동일
    #   ③ 성공: RedirectResponse("/?msg=deleted", status_code=303)
    pass
