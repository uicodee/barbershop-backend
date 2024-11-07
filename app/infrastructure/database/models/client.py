from typing import List, TYPE_CHECKING

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.database.models import BaseModel

if TYPE_CHECKING:
    from .appointment import Appointment


class Client(BaseModel):

    __tablename__ = "client"

    first_name: Mapped[str] = mapped_column(String)
    last_name: Mapped[str] = mapped_column(String, nullable=True)
    phone_number: Mapped[str] = mapped_column(String, unique=True)

    branch_id: Mapped[int] = mapped_column(ForeignKey("branch.id", ondelete="CASCADE"))
    employee_id: Mapped[int] = mapped_column(ForeignKey("employee.id", ondelete="CASCADE"))

    appointments: Mapped[List["Appointment"]] = relationship(back_populates="client", lazy="selectin")
