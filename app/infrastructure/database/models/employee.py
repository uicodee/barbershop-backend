from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING

from app.infrastructure.database.models import BaseModel

if TYPE_CHECKING:
    from .branch import Branch


class Employee(BaseModel):
    __tablename__ = "employee"

    full_name: Mapped[str] = mapped_column(String)
    email: Mapped[str] = mapped_column(String)
    password: Mapped[str] = mapped_column(String)

    branch_id: Mapped[int] = mapped_column(ForeignKey("branch.id", ondelete="CASCADE"))

    branch: Mapped["Branch"] = relationship(back_populates="employees", lazy="selectin")
