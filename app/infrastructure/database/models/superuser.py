from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.database.models import BaseModel


class Superuser(BaseModel):

    __tablename__ = "superuser"

    full_name: Mapped[str] = mapped_column(String)
    username: Mapped[str] = mapped_column(String)
    password: Mapped[str] = mapped_column(String)
