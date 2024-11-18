from fastapi import APIRouter, Depends, Path, HTTPException, status
from pydantic import PositiveInt

from app import dto
from app.api import schems
from app.api.dependencies import dao_provider, AuthProvider, get_settings, get_superuser, get_employee
from app.config import Settings
from app.infrastructure.database import HolderDao

router = APIRouter(prefix="/employee")


@router.post(
    path="/",
    description="Create a employee",
    response_model=dto.Employee,
)
async def create_employee(
        employee: schems.RegisterEmployee,
        dao: HolderDao = Depends(dao_provider),
        settings: Settings = Depends(get_settings),
) -> dto.Employee:
    auth = AuthProvider(settings=settings)
    if await dao.employee.get_employee(email=employee.email) is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Employee already exists"
        )
    return await dao.employee.add_employee(
        employee=employee, password=auth.get_password_hash(password=employee.password)
    )


@router.get(path="/", description="Get employees", response_model=list[dto.Employee])
async def get_employees(dao: HolderDao = Depends(dao_provider)) -> list[dto.Employee]:
    return await dao.employee.get_all()


@router.get(path="/me", description="Get me", response_model=dto.Employee)
async def get_me(employee: dto.Employee = Depends(get_employee)) -> dto.Employee:
    return employee


@router.get(
    path="/{employee_id}", description="Get employee", response_model=dto.Employee
)
async def get_employee(
        employee_id: PositiveInt = Path(), dao: HolderDao = Depends(dao_provider)
) -> dto.Employee:
    employee = await dao.employee.get_one(employee_id=employee_id)
    if employee is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Employee not found"
        )
    return employee


# @router.put(
#     path="/{employee_id}",
#     description="Update employee",
#     response_model=dto.Employee,
# )
# async def update_employee(
#         employee: schems.Employee,
#         employee_id: PositiveInt = Path(),
#         dao: HolderDao = Depends(dao_provider)
# ) -> dto.Employee:
#     current_employee = await dao.employee.get_one(employee_id=employee_id)
#     if current_employee is None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Employee not found")
#     return await dao.employee.update_employee(
#         employee_id=employee_id,
#         employee=employee
#     )


@router.delete(
    path="/{employee_id}",
    description="Delete employee",
)
async def delete_employee(
        employee_id: PositiveInt = Path(), dao: HolderDao = Depends(dao_provider)
):
    employee = await dao.employee.get_one(employee_id=employee_id)
    if employee is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Employee not found"
        )
    return await dao.employee.delete_employee(
        employee_id=employee_id,
    )
