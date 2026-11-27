# =====================================================================
#  회원 관리 v2 (학생용 템플릿) — 실무형 프로젝트 구조
# =====================================================================
#  v1(main.py 한 파일)에서 만든 코드를 역할별 파일로 옮기는 실습입니다.
#  👉 v1을 먼저 완성한 뒤 시작하세요. 대부분 v1 코드를 "옮기고 조금 고치는" 작업입니다.
#
#  📁 폴더 구조
#    v2/
#    ├── main.py                 ← 앱 생성 + 라우터 등록 (지금 이 파일)
#    ├── app/
#    │   ├── __init__.py         ← 비어 있어도 됨 (app 폴더를 패키지로 인식)
#    │   ├── config.py           ← ① DB 접속 정보
#    │   ├── database.py         ← ② DB 연결, get_db 의존성, 테이블 생성
#    │   ├── schemas.py          ← ③ Pydantic 모델
#    │   ├── security.py         ← ④ bcrypt
#    │   ├── crud.py             ← ⑤ SQL 함수 (conn을 매개변수로 받음!)
#    │   ├── services.py         ← ⑥ 업무 규칙
#    │   └── routers/
#    │       ├── __init__.py
#    │       ├── api_users.py    ← ⑦ JSON API (APIRouter)
#    │       └── pages.py        ← ⑧ HTML 화면 (APIRouter)
#    └── templates/              ← v1과 동일 (완성본)
#
#  📚 작업 순서: 위 폴더 구조의 ① → ⑧ 순서대로, 마지막에 이 파일(main.py)
#
#  🔑 v1과 달라지는 핵심 3가지
#    1) 파일 분리 : 다른 파일의 함수는 import 해서 사용
#                   예) from app.security import hash_password
#    2) get_db   : DB 연결을 함수 안에서 만들지 않고, FastAPI가 요청마다 넣어 줌
#                   def api_get_users(conn=Depends(get_db)):
#    3) APIRouter: @app.get 대신 router = APIRouter() 를 만들고 @router.get 사용
#                   → main.py에서 app.include_router(router)로 합침
#
#  ▶ 실행 : (v2 폴더에서) uvicorn main:app --reload
# =====================================================================

from contextlib import asynccontextmanager

from fastapi import FastAPI

# TODO 9-1: ⑦⑧을 완성한 뒤 아래 import 주석을 해제하세요.
# from app.database import init_db
# from app.routers import api_users, pages


@asynccontextmanager
async def lifespan(app: FastAPI):
    # TODO 9-2: init_db() 호출 (서버 시작 시 DB·테이블 생성)
    yield


app = FastAPI(title="회원 관리 v2", lifespan=lifespan)

# TODO 9-3: 라우터 등록
#   app.include_router(api_users.router)
#   app.include_router(pages.router)
