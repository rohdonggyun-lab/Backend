# =====================================================================
#  ⑧ routers/pages.py — HTML 화면
# =====================================================================
#  v1 STEP 8의 화면 함수 7개를 옮기면서 아래처럼 바꿉니다.
#   ✔ @app.get / @app.post   →  @router.get / @router.post
#   ✔ 각 함수 매개변수 끝에   conn=Depends(get_db)  추가  (page_signup_form 제외)
#   ✔ db_get_users()         →  crud.get_users(conn)
#   ✔ signup(...)            →  services.signup(conn, ...)
#   ✔ change_password(...)   →  services.change_password(conn, ...)
#   ✔ withdraw(...)          →  services.withdraw(conn, ...)
#   ✔ render_detail(request, user_id, ...) → render_detail(request, conn, user_id, ...)
#        내부에서 services.get_user_or_404(conn, user_id) 사용
#
#  📌 include_in_schema=False → 화면용 경로는 /docs API 문서에 표시하지 않음
# =====================================================================
from fastapi import APIRouter, Depends, Form, HTTPException, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from pydantic import ValidationError

from app import crud, services
from app.database import get_db
from app.schemas import PasswordUpdate, UserCreate

router = APIRouter(include_in_schema=False)
templates = Jinja2Templates(directory="templates")

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
    """Pydantic 검증 에러 → 한글 메시지 (완성본 제공)"""
    field = e.errors()[0]["loc"][0]
    return FIELD_ERRORS.get(field, "입력값을 확인하세요.")


# TODO 8-1: render_detail(request, conn, user_id, msg="", error="", status_code=200)

# TODO 8-2: page_index          GET  /

# TODO 8-3: page_signup_form    GET  /signup                (conn 불필요)

# TODO 8-4: page_signup         POST /signup                (Form: name, phone, password)

# TODO 8-5: page_detail         GET  /users/{user_id}

# TODO 8-6: page_change_password POST /users/{user_id}/password  (Form: current_password, new_password)

# TODO 8-7: page_withdraw       POST /users/{user_id}/delete    (Form: password)
