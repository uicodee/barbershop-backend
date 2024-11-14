from sqlalchemy.orm import sessionmaker

from app.domain.api import login, send_sms
from app.dto import AppointmentStatus
from app.infrastructure.database import HolderDao


async def send_notification(phone_number: str):
    print("[+] Running task")
    token = await login(
        email="valiyevasror10@gmail.com",
        password="bmlvvBs15HCQqP1LH8Ck68tQiQbkq4w71mGIxnjy",
    )
    await send_sms(
        token=token.data.token,
        phone_number=phone_number,
        message="Bu Eskiz dan test",
        from_="Barbershop"
    )


async def check_schedule(pool: sessionmaker, appointment_id: int, branch_id: int, employee_id: int):
    async with pool() as session:
        dao = HolderDao(session=session)
        appointment = await dao.appointment.get_one(
            appointment_id=appointment_id,
            branch_id=branch_id,
            employee_id=employee_id
        )
        if appointment is not None and appointment.status == AppointmentStatus.SCHEDULED:
            await dao.appointment.update_appointment_status(
                appointment_id=appointment_id,
                branch_id=branch_id,
                employee_id=employee_id,
                status=AppointmentStatus.MISSED
            )
