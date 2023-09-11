from dotenv import dotenv_values
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

secrets = dotenv_values(".env")
DATABASE_USER = secrets["DATABASE_USER"]
DATABASE_PASSWORD = secrets["DATABASE_PASSWORD"]

URL_DATABASE = 'postgresql://'+DATABASE_USER+':'+DATABASE_PASSWORD+'@localhost:5432/chatbot'

engine = create_engine(URL_DATABASE)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
