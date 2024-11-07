from datetime import datetime

from pydantic import Field

from app.dto import BaseModel
from .types import AppointmentStatus


class Appointment(BaseModel):

    client_id: int = Field(alias="clientId")
    appointment_date: datetime = Field(alias="appointmentDate")
    status: AppointmentStatus = Field()
    # next_sms_date: datetime = Field(alias="nextSmsDate")
