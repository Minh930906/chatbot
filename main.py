from fastapi import FastAPI

import application.models
from application.chat_router import chat_router
from application.database import engine
from application.security_router import security_router

app = FastAPI()

application.models.Base.metadata.create_all(bind=engine)

app.include_router(security_router)
app.include_router(chat_router)
