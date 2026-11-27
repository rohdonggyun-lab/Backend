# =====================================================================
#  ⑦ routers/api_users.py — JSON API (Postman으로 테스트)
# =====================================================================
#  📌 APIRouter
#     router = APIRouter(prefix="/api/users", tags=["회원 API"])
#     - prefix : 아래 모든 경로 앞에 "/api/users"가 자동으로 붙음
#                @router.get("")          → GET /api/users
#                @router.get("/{user_id}") → GET /api/users/{user_id}
#     - tags   : /docs 문서에서 묶어서 보여줄 그룹 이름
#
#  📌 Depends(get_db)
#     def api_get_users(conn=Depends(get_db)):
#     → 요청이 오면 FastAPI가 get_db()를 실행해 conn을 넣어 주고,
#       응답이 끝나면 get_db의 finally에서 연결을 닫습니다.
#
#  📌 만들 API (v1 STEP 7과 동일)
#  | 함수 이름            | 데코레이터                                                   | 매개변수
#  | api_signup           | @router.post("", response_model=UserOut, status_code=201)   | user: UserCreate
#  | api_get_users        | @router.get("", response_model=List[UserOut])               | -
#  | api_get_user         | @router.get("/{user_id}", response_model=UserOut)           | user_id: int
#  | api_change_password  | @router.put("/{user_id}/password", response_model=MessageOut) | user_id, body: PasswordUpdate
#  | api_withdraw         | @router.delete("/{user_id}", response_model=MessageOut)     | user_id, body: UserDelete
#  ※ 모든 함수의 마지막 매개변수: conn=Depends(get_db)
#  ※ summary="회원가입" 처럼 summary를 넣으면 /docs에 한글 제목이 표시됩니다.
# =====================================================================
from typing import List

from fastapi import APIRouter, Depends

from app import crud, services
from app.database import get_db
from app.schemas import MessageOut, PasswordUpdate, UserCreate, UserDelete, UserOut

# TODO 7-1: router 만들기
router = APIRouter()


# TODO 7-2: api_signup        — services.signup(conn, user) → crud.get_user(conn, new_id) 반환


# TODO 7-3: api_get_users     — crud.get_users(conn) 반환


# TODO 7-4: api_get_user      — services.get_user_or_404(conn, user_id) 반환


# TODO 7-5: api_change_password — services.change_password(...) → {"message": "비밀번호가 변경되었습니다."}


# TODO 7-6: api_withdraw      — services.withdraw(...) → {"message": "회원 탈퇴가 완료되었습니다."}
