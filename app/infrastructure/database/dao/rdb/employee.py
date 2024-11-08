from pydantic import TypeAdapter
from sqlalchemy import select, update, delete
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
            employee: schems.Employee,
            password: str
    ) -> dto.Employee:
        employee = Employee(
            full_name=employee.full_name,
            email=employee.email,
            password=password,
            branch_id=employee.branch_id
        )
        self.session.add(employee)
        await self.session.commit()
        result = await self.session.execute(select(Employee).where(Employee.id == employee.id))
        return dto.Employee.from_orm(result.scalar())

    async def get_one(
            self,
            employee_id: int,
    ) -> dto.Employee | dto.EmployeeWithPassword:
        result = await self.session.execute(
            select(Employee).where(Employee.id == employee_id)
        )
        employee = result.scalar()
        if employee is not None:
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

    async def get_all(self) -> list[dto.Employee]:
        result = await self.session.execute(select(Employee))
        adapter = TypeAdapter(list[dto.Employee])
        return adapter.validate_python(result.scalars().all())

    async def get_all_by_branch(self, branch_id: int) -> list[dto.Employee]:
        result = await self.session.execute(select(Employee).where(
            Employee.branch_id == branch_id
        ))
        adapter = TypeAdapter(list[dto.Employee])
        return adapter.validate_python(result.scalars().all())

    async def update_employee(self, employee_id: int, employee: schems.Employee) -> dto.Employee:
        result = await self.session.execute(
            update(Employee).where(
                Employee.id == employee_id
            )
            .values(**employee.dict())
            .returning(Employee)
        )
        await self.session.commit()
        return dto.Employee.model_validate(result.scalar())

    async def delete_employee(self, employee_id: int) -> None:
        await self.session.execute(delete(Employee).where(
            Employee.id == employee_id,
        ))
        await self.session.commit()
