from datetime import datetime

from pydantic import Field, BaseModel, PositiveInt, field_validator


class Appointment(BaseModel):
    client_id: PositiveInt = Field(alias="clientId")
    appointment_date: str = Field(alias="appointmentDate")

    @field_validator("appointment_date", mode="before")
    def validate_and_convert_date(cls, value):
        if isinstance(value, str):
            try:
                datetime.strptime(value, "%d.%m.%Y %H:%M")
            except ValueError:
                raise ValueError("Incorrect date format, should be 'DD.MM.YYYY HH:MM'")
        return value


class UpdateAppointment(BaseModel):

    appointment_date: str = Field(alias="appointmentDate")

    @field_validator("appointment_date", mode="before")
    def validate_and_convert_date(cls, value):
        if isinstance(value, str):
            try:
                datetime.strptime(value, "%d.%m.%Y %H:%M")
            except ValueError:
                raise ValueError("Incorrect date format, should be 'DD.MM.YYYY HH:MM'")
        return value
