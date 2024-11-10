from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from app.infrastructure.database.models import BaseModel


class ClientAppointment(BaseModel):
    __tablename__ = "client_appointment"

    client_id: Mapped[int] = mapped_column(ForeignKey("client.id", ondelete="CASCADE"))
    appointment_id: Mapped[int] = mapped_column(ForeignKey("appointment.id", ondelete="CASCADE"))
