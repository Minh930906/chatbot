from fastapi import FastAPI

import application.models
from application.chat_router import chat_router
from application.database import engine, SessionLocal
from application.security_router import security_router
from application.init_db import create_Chat_Bot_User

app = FastAPI()
db = SessionLocal()
create_Chat_Bot_User(db)

application.models.Base.metadata.create_all(bind=engine)

app.include_router(security_router)
app.include_router(chat_router)
