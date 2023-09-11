import openai
from dotenv import dotenv_values
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import application.models
from application import auth, schemas
from application.database import get_db
from application.utils import rate_limiting

chat_router = APIRouter()
secrets = dotenv_values(".env")

api_key = secrets["CHATGPT_API_KEY"]
openai.api_key = api_key


@chat_router.post("/chat/")
async def chat(request: schemas.ChatRequest,
               current_user: schemas.UserInDB = Depends(auth.get_current_user),
               db: Session = Depends(get_db),
               rate_limit: int = Depends(rate_limiting)):
    # A chat üzenet
    user_message = request.message_text

    waiting_for_bot_response = True

    # Hívja meg a GPT-3.5 modellt
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

    # Az AI válasza
    ai_message = request.choices[0].message.content

    return {"ai_message": ai_message}


@chat_router.get("/chat/{user_id}", response_model=schemas.UserWithMessages)
def get_user_messages(user_id: int, db: Session = Depends(get_db)):
    user = db.query(application.models.User).filter(application.models.User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="Felhasználó nem található")

    # Az üzenetek előzményeit maximum 500 szóra szűkítjük
    messages = db.query(application.models.Message).filter(application.models.Message.owner_id == user_id).all()
    message_history = ""
    message_word_count = 0
    for message in messages:
        if message_word_count + len(message.text.split()) <= 500:
            message_history += message.text + " "
            message_word_count += len(message.text.split())
        else:
            break
    print(message_word_count)
    return {"user": user.username, "message_history": message_history}
