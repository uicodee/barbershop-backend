from datetime import datetime
from sqlalchemy import ForeignKey, DateTime, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING

from app import dto
from app.infrastructure.database.models import BaseModel

if TYPE_CHECKING:
    from .client import Client


class Appointment(BaseModel):
    __tablename__ = "appointment"

    client_id: Mapped[int] = mapped_column(ForeignKey("client.id", ondelete="CASCADE"))
    branch_id: Mapped[int] = mapped_column(ForeignKey("branch.id", ondelete="CASCADE"))
    employee_id: Mapped[int] = mapped_column(
        ForeignKey("employee.id", ondelete="CASCADE")
    )
    message_template_id: Mapped[int] = mapped_column(
        ForeignKey("message_template.id", ondelete="CASCADE")
    )

    appointment_date: Mapped[datetime] = mapped_column(DateTime(True))

    status: Mapped[dto.AppointmentStatus] = mapped_column(
        Enum(dto.AppointmentStatus), default=dto.AppointmentStatus.SCHEDULED
    )

    client: Mapped["Client"] = relationship(
        "Client", foreign_keys="Appointment.client_id"
    )
