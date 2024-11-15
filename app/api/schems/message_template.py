from pydantic import BaseModel


class MessageTemplate(BaseModel):

    text: str
