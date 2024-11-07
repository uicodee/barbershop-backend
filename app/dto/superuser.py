from pydantic import Field

from app.dto import Base


class Superuser(Base):

    full_name: str = Field(alias="fullName")
    username: str = Field()


class SuperuserWithPassword(Superuser):
    password: str
