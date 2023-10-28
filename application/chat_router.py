import openai
from dotenv import dotenv_values
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

import application.models
from application import auth, schemas
from application.database import get_db
from application.schemas import MessageResponse
from application.utils import rate_limiting

chat_router = APIRouter()
secrets = dotenv_values(".env")

api_key = secrets["CHATGPT_API_KEY"]
openai.api_key = api_key


@chat_router.post("/chat/", response_model=MessageResponse)
async def chat(request: schemas.ChatRequest,
               current_user: schemas.UserInDB = Depends(auth.get_current_user),
               db: Session = Depends(get_db),
               rate_limit: int = Depends(rate_limiting)):
    user_message = request.message_text
    recent_messages = db.query(application.models.Message).order_by(application.models.Message.created_at.asc()).limit(
        10).all()
    messages = [{"role": "system", "content": "You are a helpful assistant"}]

    for message in recent_messages:
        role = "user" if message.owner_id == current_user.id else "assistant" if message.owner_id == 3 else "user"
        messages.append({"role": role, "content": message.text})

    messages.append({"role": "user", "content": user_message})

    request = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        max_tokens=100
    )

    db_message = application.models.Message(text=user_message, owner_id=current_user.id)
    db.add(db_message)
    db.commit()
    db.refresh(db_message)

    ai_message = request.choices[0].message.content
    chatbot = db.query(application.models.User).filter(application.models.User.username == 'ChatBot').first()
    chat_bot_message = application.models.Message(text=ai_message, owner_id=chatbot.id)
    db.add(chat_bot_message)
    db.commit()
    db.refresh(chat_bot_message)
    messages = db.query(application.models.Message).all()
    message_history = ""
    for message in messages:
        user = db.query(application.models.User).filter(application.models.User.id == message.owner_id).first()
        message_history += user.username + ": " + message.text + "\n"

    return {"respond": message_history}


@chat_router.get("/chat_history")
def get_user_messages(db: Session = Depends(get_db)):
    messages = db.query(application.models.Message).all()
    message_history = ""
    for message in messages:
        user = db.query(application.models.User).filter(application.models.User.id == message.owner_id).first()
        message_history += user.username + ": " + message.text + "\n"

    return message_history
