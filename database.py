from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base


DATABASE_URL = "sqlite:///games.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    """Create all tables in the database."""
    Base.metadata.create_all(bind=engine)
    print("Database created successfully.")

if __name__ == "__main__":
    init_db()