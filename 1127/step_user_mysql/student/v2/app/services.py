# =====================================================================
#  ⑥ services.py — 업무 규칙 (API와 HTML 화면이 함께 사용)
# =====================================================================
#  crud.py는 "SQL만", services.py는 "규칙 판단(중복, 본인 확인 등)"을 담당합니다.
#  v1 STEP 6의 함수를 옮기면서
#   ✔ 첫 번째 매개변수로 conn을 받고
#   ✔ db_create_user(...)  →  crud.create_user(conn, ...)  처럼 바꿉니다.
# =====================================================================
import pymysql
from fastapi import HTTPException

from app import crud
from app.schemas import UserCreate
from app.security import hash_password, verify_password


def signup(conn, data: UserCreate) -> int:
    # TODO 6-1: v1 signup 옮기기
    #   except pymysql.err.IntegrityError: 에서 raise 전에 conn.rollback() 추가
    #   (실패한 작업을 취소해서 연결을 깨끗한 상태로 되돌림)
    pass


def get_user_or_404(conn, user_id: int) -> dict:
    # TODO 6-2: (새 함수) crud.get_user → None이면 404 "회원을 찾을 수 없습니다." → 아니면 user 반환
    #   API 상세 조회와 HTML 상세 화면에서 함께 사용합니다.
    pass


def check_password(conn, user_id: int, password: str) -> None:
    # TODO 6-3: v1 check_password 옮기기
    pass


def change_password(conn, user_id: int, current_pw: str, new_pw: str) -> None:
    # TODO 6-4: v1 change_password 옮기기
    pass


def withdraw(conn, user_id: int, password: str) -> None:
    # TODO 6-5: v1 withdraw 옮기기
    pass
