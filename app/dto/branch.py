from pydantic import Field

from app.dto import BaseModelWithDateTime


class Branch(BaseModelWithDateTime):

    name: str = Field()
    location: str = Field()
