from datetime import datetime

from sqlalchemy import ForeignKey, DateTime, Enum
from sqlalchemy.orm import Mapped, mapped_column

from app import dto
from app.infrastructure.database.models import BaseModel


class SMSReminder(BaseModel):

    __tablename__ = "sms_reminder"

    appointment_id: Mapped[int] = mapped_column(ForeignKey("appointment.id", ondelete="CASCADE"))
    sent_at: Mapped[datetime] = mapped_column(DateTime)
    status: Mapped[dto.ReminderStatus] = mapped_column(Enum(dto.ReminderStatus))
