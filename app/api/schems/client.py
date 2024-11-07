from pydantic import Field, BaseModel


class Client(BaseModel):
    first_name: str = Field(alias="firstName")
    last_name: str | None = Field(default=None, alias="lastName")
    phone_number: str = Field(alias="phoneNumber")
