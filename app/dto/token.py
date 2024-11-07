from pydantic import Field

from app.dto import Base


class Token(Base):
    access_token: str = Field(alias="accessToken")
    refresh_token: str = Field(alias="refreshToken")
    type: str
