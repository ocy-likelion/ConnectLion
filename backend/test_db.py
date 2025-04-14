from app.db.base import engine
from sqlalchemy import text

def test_connection():
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            print("데이터베이스 연결 성공!")
            return True
    except Exception as e:
        print(f"데이터베이스 연결 실패: {str(e)}")
        return False

if __name__ == "__main__":
    test_connection() 