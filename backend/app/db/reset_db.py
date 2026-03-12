from sqlalchemy import text
from app.db.session import engine
from app.db.base import Base  # if you have one
from app.db.models import Receipt, ReceiptJob, User  # import your models

# TO RUN: python -m app.db.reset_db

def reset_tables():
    with engine.connect() as conn:
        # Drop tables if they exist
        conn.execute(text("DROP TABLE IF EXISTS receipts"))
        conn.execute(text("DROP TABLE IF EXISTS receipt_jobs"))
        # Optionally: drop users table if needed
        # conn.execute(text("DROP TABLE IF EXISTS users"))
        conn.commit()
        print("Tables dropped successfully.")

    # Recreate tables
    Base.metadata.create_all(bind=engine)
    print("Tables recreated successfully.")

if __name__ == "__main__":
    reset_tables()