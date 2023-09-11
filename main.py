from fastapi import FastAPI, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

import application.models
from application import auth, schemas
from application.chat_router import chat_router
from application.database import engine
from application.database import get_db
from application.security_router import security_router
from application.utils import rate_limiting

app = FastAPI()

application.models.Base.metadata.create_all(bind=engine)

app.include_router(security_router)
app.include_router(chat_router)

user_request_count = {}

MAX_REQUESTS_PER_MINUTE = 3


# class MessageBase(BaseModel):
#     message_text: str
#
#
# @app.post("/valami")
# async def send_message(message: MessageBase,
#                        current_user: schemas.UserInDB = Depends(application.auth.get_current_user),
#                        db: Session = Depends(get_db),
#                        rate_limit: int = Depends(rate_limiting)
#                        ):
#     print(current_user.username)
#
#     db_message = application.models.Message(text=message.message_text)
#     db.add(db_message)
#     db.commit()
#     db.refresh(db_message)
