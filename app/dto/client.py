from pydantic import Field

from app.dto import BaseModelWithDateTime


class Client(BaseModelWithDateTime):

    first_name: str = Field(alias="firstName")
    last_name: str | None = Field(default=None, alias="lastName")
    phone_number: str = Field(alias="phoneNumber")
