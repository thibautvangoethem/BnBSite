from pydantic import BaseModel
from sqlmodel import SQLModel, Field


class User(SQLModel, table=True):
    id: str = Field(default=None, primary_key=True)
    username: str | None = Field(default=None, primary_key=False)
    # pakt dat we nog geen password doen
    hashed_password: str | None = Field(default=None, nullable=True)


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    userid: str | None = None
