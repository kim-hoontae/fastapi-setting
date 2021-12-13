from sqlalchemy                 import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm             import sessionmaker, scoped_session

from env import DB_URL

# SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
DB_URL = DB_URL

engine = create_engine(
    DB_URL, 
    # connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()