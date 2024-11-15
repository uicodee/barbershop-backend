from typing import TYPE_CHECKING
from sqlalchemy import String, ForeignKey, Integer
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
    employee_id: Mapped[int] = mapped_column(
        ForeignKey("employee.id", ondelete="CASCADE")
    )
    period: Mapped[int] = mapped_column(Integer, default=30)

    next_appointment_id: Mapped[int] = mapped_column(
        ForeignKey("appointment.id", ondelete="SET NULL"), nullable=True
    )

    next_appointment: Mapped["Appointment"] = relationship(
        "Appointment",
        foreign_keys="Client.next_appointment_id",
        uselist=False,
        post_update=True,
        lazy="selectin",
    )
