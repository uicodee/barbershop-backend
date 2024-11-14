from pydantic import TypeAdapter
from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app import dto
from app.api import schems
from app.infrastructure.database.dao.rdb import BaseDAO
from app.infrastructure.database.models import Client


class ClientDAO(BaseDAO[Client]):
    def __init__(self, session: AsyncSession):
        super().__init__(Client, session)

    async def create(
            self,
            branch_id: int,
            employee_id: int,
            client: schems.Client
    ) -> dto.Client:
        client = Client(
            **client.dict(),
            branch_id=branch_id,
            employee_id=employee_id
        )
        self.session.add(client)
        await self.session.commit()
        return dto.Client.from_orm(client)

    async def get_all(self, employee_id: int, branch_id: int) -> list[dto.Client]:
        result = await self.session.execute(select(Client).where(
            Client.branch_id == branch_id,
            Client.employee_id == employee_id,
        ))
        adapter = TypeAdapter(list[dto.Client])
        return adapter.validate_python(result.scalars().all())

    async def get_by_phone_number(
            self,
            phone_number: str,
            employee_id: int
    ) -> dto.Client:
        result = await self.session.execute(
            select(Client).where(
                Client.phone_number == phone_number,
                Client.employee_id == employee_id
            )
        )
        client = result.scalar()
        if client is not None:
            return dto.Client.from_orm(client)

    async def get_client(
            self,
            employee_id: int,
            client_id: int,
            branch_id: int
    ) -> dto.Client:
        result = await self.session.execute(
            select(Client).where(
                Client.id == client_id,
                Client.branch_id == branch_id,
                Client.employee_id == employee_id
            )
        )
        client = result.scalar()
        if client is not None:
            return dto.Client.from_orm(client)

    async def update_appointment(self, client_id: int, employee_id: int, next_appointment_id: int) -> dto.Client:
        result = await self.session.execute(
            update(Client).where(
                Client.id == client_id,
                Client.employee_id == employee_id
            )
            .values(next_appointment_id=next_appointment_id)
            .returning(Client)
        )
        await self.session.commit()
        return dto.Client.model_validate(result.scalar())

    async def update_client_period(self, client_id: int, employee_id: int, branch_id: int, period: int) -> dto.Client:
        result = await self.session.execute(
            update(Client).where(
                Client.id == client_id,
                Client.employee_id == employee_id,
                Client.branch_id == branch_id
            )
            .values(period=period)
            .returning(Client)
        )
        await self.session.commit()
        return dto.Client.model_validate(result.scalar())

    async def update_client(self, client_id: int, employee_id: int, client: schems.Client) -> dto.Client:
        result = await self.session.execute(
            update(Client).where(
                Client.id == client_id,
                Client.employee_id == employee_id
            )
            .values(**client.dict())
            .returning(Client)
        )
        await self.session.commit()
        return dto.Client.model_validate(result.scalar())

    async def delete_client(self, client_id: int, branch_id: int, employee_id: int) -> None:
        await self.session.execute(delete(Client).where(
            Client.id == client_id,
            Client.branch_id == branch_id,
            Client.employee_id == employee_id,
        ))
        await self.session.commit()
