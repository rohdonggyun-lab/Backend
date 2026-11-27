# =====================================================================
#  ⑤ crud.py — SQL 실행 함수 (DB 작업만 담당)
# =====================================================================
#  v1 STEP 5의 db_xxx 함수를 옮기면서 아래처럼 바꿉니다.
#
#   v1                                      v2
#   def db_get_user(user_id):               def get_user(conn, user_id):
#       with get_connection() as conn:          with conn.cursor() as cur:
#           with conn.cursor() as cur:              ...
#               ...
#
#  ✔ 함수 이름에서 db_ 제거  (crud.get_user 처럼 파일 이름이 앞에 붙으므로)
#  ✔ 첫 번째 매개변수로 conn을 받음
#  ✔ with get_connection() 줄 삭제 — 연결은 get_db가 열고 닫음 (여기서 닫지 않기!)
#  ✔ INSERT/UPDATE/DELETE 후 conn.commit()은 그대로
# =====================================================================


def create_user(conn, name: str, phone: str, hashed_pw: str) -> int:
    # TODO 5-1: INSERT → new_id = cur.lastrowid → commit → new_id 반환
    pass


def get_users(conn) -> list:
    # TODO 5-2: SELECT id, name, phone, created_at ... ORDER BY id DESC → fetchall
    pass


def get_user(conn, user_id: int):
    # TODO 5-3: SELECT ... WHERE id = %s → fetchone
    pass


def get_password_hash(conn, user_id: int):
    # TODO 5-4: SELECT password ... → row["password"] 또는 None
    pass


def update_password(conn, user_id: int, hashed_pw: str) -> None:
    # TODO 5-5: UPDATE ... → commit
    pass


def delete_user(conn, user_id: int) -> None:
    # TODO 5-6: DELETE ... → commit
    pass
