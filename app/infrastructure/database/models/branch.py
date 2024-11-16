from typing import List, TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.database.models import BaseModel

if TYPE_CHECKING:
    from .employee import Employee
    from .message_template import MessageTemplate


class Branch(BaseModel):
    __tablename__ = "branch"

    name: Mapped[str] = mapped_column(String)
    location: Mapped[str] = mapped_column(String)

    employees: Mapped[List["Employee"]] = relationship(back_populates="branch")
    message_templates: Mapped[List["MessageTemplate"]] = relationship(back_populates="branch", lazy="selectin")
