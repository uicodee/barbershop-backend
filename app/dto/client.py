from pydantic import Field

from app.dto import BaseModelWithDateTime
from .appointment import Appointment


class Client(BaseModelWithDateTime):

    first_name: str = Field(alias="firstName")
    last_name: str | None = Field(default=None, alias="lastName")
    phone_number: str = Field(alias="phoneNumber")
    period: int = Field()
    next_appointment: Appointment | None = Field(default=None, alias="nextAppointment")
