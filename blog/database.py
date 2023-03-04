from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///.blog.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(
    bind=engine,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# You can learn more about it from the docs of fast api
# https://fastapi.tiangolo.com/tutorial/sql-databases/


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
