from sqlalchemy import text

from app.infrastructure.database.session import SessionLocal


def test_database_connection() -> None:
    db = SessionLocal()

    try:
        result = db.execute(text("SELECT 1")).scalar()
        assert result == 1
    finally:
        db.close()