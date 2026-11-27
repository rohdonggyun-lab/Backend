# =====================================================================
#  ② database.py — DB 연결 / get_db 의존성 / 테이블 생성
# =====================================================================
import pymysql

from app import config


def get_connection(with_db: bool = True):
    # TODO 2-1: pymysql.connect(...)를 반환하세요.
    #   host=config.DB_HOST, port=config.DB_PORT, user=config.DB_USER,
    #   password=config.DB_PASSWORD,
    #   database=config.DB_NAME if with_db else None,   ← DB 생성 전에는 None으로 접속
    #   charset="utf8mb4", cursorclass=pymysql.cursors.DictCursor
    pass


def get_db():
    # TODO 2-2: FastAPI 의존성 함수 (Depends(get_db)로 사용)
    #   ① conn = get_connection()
    #   ② try:     yield conn        ← 라우터 함수에 연결을 넘겨줌 (return 아님!)
    #   ③ finally: conn.close()      ← 응답이 끝나면 반드시 연결 닫기
    pass


# TODO 2-3: v1의 CREATE_USER_TABLE SQL을 그대로 옮기세요.
CREATE_USER_TABLE = """
"""


def init_db():
    # TODO 2-4: v1의 init_db()를 옮기고 아래처럼 고치세요.
    #   - DB 생성 시   : with get_connection(with_db=False) as conn:
    #   - DB 이름      : config.DB_NAME
    #   - 테이블 생성 시: with get_connection() as conn:
    pass
