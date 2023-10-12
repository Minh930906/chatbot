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

    request = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": user_message}
        ],
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
    message_word_count = 0
    for message in messages:
        user = db.query(application.models.User).filter(application.models.User.id == message.owner_id).first()
        if message_word_count + len(message.text.split()) <= 500:
            message_history += user.username + ": " + message.text + "\n"
            message_word_count += len(message.text.split())
        else:
            break
    return message_history
