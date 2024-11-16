from pydantic import Field

from app.dto import BaseModelWithDateTime
from .message_template import MessageTemplate


class Branch(BaseModelWithDateTime):

    name: str = Field()
    location: str = Field()

    message_templates: list[MessageTemplate] = Field(default=[], alias="messageTemplates")
