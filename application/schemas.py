from typing import Optional

from pydantic import BaseModel


class UserBase(BaseModel):
    email: str
    username: str

class UserWithMessages(BaseModel):
    user: str
    message_history: str


class UserIn(UserBase):
    password: str


class UserInDBBase(UserBase):
    id: int

    class Config:
        orm_mode: True


class UserInDB(UserInDBBase):
    hashed_password: str


class TokenData(BaseModel):
    username: Optional[str] = None


class Token(BaseModel):
    access_token: str
    token_type: str


class ChatRequest(BaseModel):
    message_text: str
