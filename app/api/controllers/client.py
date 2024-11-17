from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.params import Path
from pydantic import PositiveInt

from app import dto
from app.api import schems
from app.api.dependencies import dao_provider, get_employee
from app.infrastructure.database import HolderDao

router = APIRouter(prefix="/client")


@router.post(
    path="/",
    description="Create a client",
    response_model=dto.Client,
)
async def create_client(
    client: schems.Client,
    employee: dto.Employee = Depends(get_employee),
    dao: HolderDao = Depends(dao_provider),
) -> dto.Client:
    if (
        await dao.client.get_by_phone_number(
            phone_number=client.phone_number, employee_id=employee.id
        )
        is not None
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Client already exists"
        )
    return await dao.client.create(
        client=client, branch_id=employee.branch.id, employee_id=employee.id
    )


@router.get(path="/", description="Get clients", response_model=list[dto.Client])
async def get_clients(
    employee: dto.Employee = Depends(get_employee),
    dao: HolderDao = Depends(dao_provider),
) -> list[dto.Client]:
    return await dao.client.get_all(
        branch_id=employee.branch.id, employee_id=employee.id
    )


@router.get(path="/{client_id}", description="Get client", response_model=dto.Client)
async def get_client(
    employee: dto.Employee = Depends(get_employee),
    client_id: PositiveInt = Path(),
    dao: HolderDao = Depends(dao_provider),
) -> dto.Client:
    client = await dao.client.get_client(
        client_id=client_id, branch_id=employee.branch.id, employee_id=employee.id
    )
    if client is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Client not found"
        )
    return client


@router.put(
    path="/{client_id}",
    description="Update client",
    response_model=dto.Client,
)
async def update_client(
    client: schems.Client,
    employee: dto.Employee = Depends(get_employee),
    client_id: PositiveInt = Path(),
    dao: HolderDao = Depends(dao_provider),
) -> dto.Client:
    current_client = await dao.client.get_client(
        client_id=client_id, branch_id=employee.branch.id, employee_id=employee.id
    )
    if current_client is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Client not found"
        )
    return await dao.client.update_client(
        client_id=client_id, employee_id=employee.id, client=client
    )


@router.delete(
    path="/{client_id}",
    description="Delete client",
)
async def delete_client(
    employee: dto.Employee = Depends(get_employee),
    client_id: PositiveInt = Path(),
    dao: HolderDao = Depends(dao_provider),
):
    client = await dao.client.get_client(
        client_id=client_id, branch_id=employee.branch.id, employee_id=employee.id
    )
    if client is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Client not found"
        )
    return await dao.client.delete_client(
        client_id=client_id, branch_id=employee.branch.id, employee_id=employee.id
    )
