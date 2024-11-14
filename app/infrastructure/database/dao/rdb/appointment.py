from datetime import datetime, timezone

from pydantic import TypeAdapter
from sqlalchemy import select, update, delete, desc, asc
from sqlalchemy.ext.asyncio import AsyncSession

from app import dto
from app.api import schems
from app.infrastructure.database.dao.rdb import BaseDAO
from app.infrastructure.database.models import Appointment


class AppointmentDAO(BaseDAO[Appointment]):
    def __init__(self, session: AsyncSession):
        super().__init__(Appointment, session)

    async def create(
            self,
            appointment: schems.Appointment,
            branch_id: int,
            employee_id: int
    ) -> dto.Appointment:
        appointment = Appointment(
            client_id=appointment.client_id,
            appointment_date=datetime.strptime(appointment.appointment_date, "%d.%m.%Y %H:%M").replace(
                tzinfo=timezone.utc),
            branch_id=branch_id,
            employee_id=employee_id
        )
        self.session.add(appointment)
        await self.session.commit()
        return dto.Appointment.from_orm(appointment)

    async def get_all(self, branch_id: int, employee_id: int) -> list[dto.Appointment]:
        result = await self.session.execute(
            select(Appointment)
            .where(
                Appointment.branch_id == branch_id,
                Appointment.employee_id == employee_id
            )
            .order_by(asc(Appointment.appointment_date), desc(Appointment.created_at))
        )

        adapter = TypeAdapter(list[dto.Appointment])
        return adapter.validate_python(result.scalars().all())

    async def get_one(
            self,
            appointment_id: int,
            branch_id: int,
            employee_id: int
    ) -> dto.Appointment:
        result = await self.session.execute(
            select(Appointment).where(
                Appointment.id == appointment_id,
                Appointment.branch_id == branch_id,
                Appointment.employee_id == employee_id
            )
        )
        appointment = result.scalar()
        if appointment is not None:
            return dto.Appointment.from_orm(appointment)

    async def get_client_all(self, client_id: int, branch_id: int, employee_id: int) -> list[dto.Appointment]:
        result = await self.session.execute(select(Appointment).where(
            Appointment.client_id == client_id,
            Appointment.branch_id == branch_id,
            Appointment.employee_id == employee_id,
        ))
        adapter = TypeAdapter(list[dto.Appointment])
        return adapter.validate_python(result.scalars().all())

    async def update_appointment_status(
            self,
            employee_id: int,
            branch_id: int,
            appointment_id: int,
            status: dto.AppointmentStatus
    ) -> dto.Appointment:
        result = await self.session.execute(
            update(Appointment).where(
                Appointment.id == appointment_id,
                Appointment.employee_id == employee_id,
                Appointment.branch_id == branch_id,
            )
            .values(
                status=status
            )
            .returning(Appointment)
        )
        await self.session.commit()
        return dto.Appointment.model_validate(result.scalar())

    async def update_appointment(
            self,
            employee_id: int,
            branch_id: int,
            appointment_id: int,
            appointment: schems.UpdateAppointment
    ) -> dto.Appointment:
        result = await self.session.execute(
            update(Appointment).where(
                Appointment.id == appointment_id,
                Appointment.employee_id == employee_id,
                Appointment.branch_id == branch_id,
            )
            .values(
                appointment_date=datetime.strptime(appointment.appointment_date, "%d.%m.%Y %H:%M").replace(
                    tzinfo=timezone.utc
                )
            )
            .returning(Appointment)
        )
        await self.session.commit()
        return dto.Appointment.model_validate(result.scalar())

    async def delete_appointment(
            self,
            client_id: int,
            branch_id: int,
            employee_id: int,
            appointment_id: int
    ) -> None:
        await self.session.execute(
            delete(Appointment).where(
                Appointment.id == appointment_id,
                Appointment.client_id == client_id,
                Appointment.branch_id == branch_id,
                Appointment.employee_id == employee_id,
            )
        )
        await self.session.commit()
