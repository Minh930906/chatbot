from sqlalchemy.orm import Session

import application.models

def create_Chat_Bot_User(db: Session):
    chatbot = db.query(application.models.User).filter(application.models.User.username == 'ChatBot').first()
    if not chatbot:
        chatbot = application.models.User(username="ChatBot")
        db.add(chatbot)

    db.commit()
    db.refresh(chatbot)