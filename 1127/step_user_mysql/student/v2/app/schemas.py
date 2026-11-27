# =====================================================================
#  ③ schemas.py — Pydantic 모델 (요청 검증 / 응답 형식)
# =====================================================================
#  v1 STEP 4의 모델 4개를 그대로 옮기고, MessageOut을 새로 만듭니다.
# =====================================================================
from datetime import datetime

from pydantic import BaseModel, Field

PHONE_PATTERN = r"^010-\d{4}-\d{4}$"


class UserCreate(BaseModel):
    # TODO 3-1: name(1~50자) / phone(PHONE_PATTERN) / password(8~20자) — 모두 필수
    pass


class UserOut(BaseModel):
    # TODO 3-2: id / name / phone / created_at  (password 없음!)
    pass


class PasswordUpdate(BaseModel):
    # TODO 3-3: current_password / new_password(8~20자)
    pass


class UserDelete(BaseModel):
    # TODO 3-4: password
    pass


class MessageOut(BaseModel):
    # TODO 3-5: message(str) — 수정·탈퇴 API의 응답 모델로 사용
    pass
