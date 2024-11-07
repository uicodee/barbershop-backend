from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app import dto
from app.api import schems
from app.infrastructure.database.dao.rdb import BaseDAO
from app.infrastructure.database.models import Employee


class EmployeeDAO(BaseDAO[Employee]):
    def __init__(self, session: AsyncSession):
        super().__init__(Employee, session)

    async def add_employee(
            self,
            employee: schems.Employee
    ) -> dto.Employee:
        employee = Employee(**employee.dict())
        self.session.add(employee)
        await self.session.commit()
        return dto.Employee.from_orm(employee)

    async def get_employee(
            self,
            email: str,
            with_password: bool = False
    ) -> dto.Employee | dto.EmployeeWithPassword:
        result = await self.session.execute(
            select(Employee).where(Employee.email == email)
        )
        employee = result.scalar()
        if employee is not None:
            if with_password:
                return dto.EmployeeWithPassword.from_orm(employee)
            else:
                return dto.Employee.from_orm(employee)
