-- =====================================================================
--  회원 관리 — DB / user 테이블 생성 SQL
--  MySQL Workbench 또는 mysql 명령줄에서 실행
--  (FastAPI 서버도 시작할 때 init_db()로 같은 작업을 자동 수행합니다)
-- =====================================================================

-- 1) 데이터베이스 생성 (한글·이모지 저장을 위해 utf8mb4)
CREATE DATABASE IF NOT EXISTS fastapi_db
    DEFAULT CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE fastapi_db;

-- 2) user 테이블 생성
CREATE TABLE IF NOT EXISTS user (
    id         INT AUTO_INCREMENT PRIMARY KEY,   -- 회원 번호 (자동 증가)
    name       VARCHAR(50)  NOT NULL,            -- 이름
    phone      VARCHAR(13)  NOT NULL UNIQUE,     -- 휴대폰 (010-1234-5678, 중복 불가)
    password   VARCHAR(255) NOT NULL,            -- bcrypt 해시 (60자)
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,                              -- 가입일
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP   -- 수정일 (자동 갱신)
);

-- =====================================================================
--  데이터 확인용 SQL (Postman / 화면에서 작업한 뒤 실행해 보세요)
-- =====================================================================
-- 전체 회원 조회
SELECT * FROM user;

-- 비밀번호 수정 확인: password 해시와 updated_at이 바뀌었는지
SELECT id, name, password, created_at, updated_at FROM user WHERE id = 1;

-- 탈퇴 확인: 결과가 0건이면 삭제된 것
SELECT COUNT(*) FROM user WHERE id = 2;

-- 테이블 구조 확인
DESC user;

-- (초기화가 필요할 때만) 모든 데이터 삭제 + 번호 1부터 다시
-- TRUNCATE TABLE user;
