import uuid

from pydantic import BaseModel


class Token(BaseModel):
    token: str


class ApiLogin(BaseModel):
    message: str
    data: Token
    token_type: str


class ApiSend(BaseModel):
    id: uuid.UUID
    message: str
    status: str
