from datetime import datetime

from pydantic import Field, BaseModel, PositiveInt, field_validator


class Appointment(BaseModel):
    client_id: PositiveInt = Field(alias="clientId")
    appointment_date: str = Field(alias="appointmentDate")

    @field_validator("appointment_date", mode="before")
    def validate_and_convert_date(cls, value):
        if isinstance(value, str):
            try:
                date = datetime.strptime(value, "%d.%m.%Y %H:%M")
                cls.check_future_date(date)
                return date
            except ValueError:
                raise ValueError("Incorrect date format, should be 'DD.MM.YYYY HH:MM'")
        return value

    @staticmethod
    def check_future_date(date: datetime):
        current_time = datetime.now()
        if date <= current_time:
            raise ValueError(f"Date should be in the future. Current time: {current_time.strftime('%d.%m.%Y %H:%M')}")


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
