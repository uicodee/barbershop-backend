from datetime import datetime, timedelta

from pytz import timezone
from apscheduler_di import ContextSchedulerDecorator
from fastapi import APIRouter, Depends, Path, HTTPException, status, Query
from pydantic import PositiveInt

from app import dto
from app.api import schems
from app.api.dependencies import dao_provider, get_employee, get_scheduler
from app.domain.schedule import send_notification, check_schedule
from app.infrastructure.database import HolderDao

router = APIRouter(prefix="/appointment")


@router.post(
    path="/",
    description="Create an appointment",
    response_model=dto.Appointment,
)
async def create_appointment(
        appointment: schems.Appointment,
        employee: dto.Employee = Depends(get_employee),
        scheduler: ContextSchedulerDecorator = Depends(get_scheduler),
        dao: HolderDao = Depends(dao_provider)
) -> dto.Appointment:
    client = await dao.client.get_client(
        client_id=appointment.client_id,
        branch_id=employee.branch.id,
        employee_id=employee.id
    )
    if client is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Client not found",
        )
    appointment_date = datetime.strptime(appointment.appointment_date, "%d.%m.%Y %H:%M").astimezone(timezone('UTC'))
    next_appointment = await dao.appointment.create(
        appointment=appointment,
        branch_id=employee.branch.id,
        employee_id=employee.id
    )
    scheduler.add_job(
        send_notification,
        "date",
        run_date=appointment_date,
        kwargs={
            "phone_number": client.phone_number
        }
    )
    scheduler.add_job(
        check_schedule,
        "date",
        run_date=appointment_date + timedelta(hours=1),
        kwargs={
            "appointment_id": next_appointment.id,
            "branch_id": employee.branch.id,
            "employee_id": employee.id,
        }
    )
    await dao.client.update_appointment(
        client_id=client.id,
        employee_id=employee.id,
        next_appointment_id=next_appointment.id,
    )
    return next_appointment


@router.get(
    path="/",
    description="Get client appointments",
    response_model=list[dto.Appointment],
)
async def get_appointments(
        employee: dto.Employee = Depends(get_employee),
        dao: HolderDao = Depends(dao_provider),
) -> list[dto.Appointment]:
    return await dao.appointment.get_all(
        branch_id=employee.branch.id,
        employee_id=employee.id
    )


@router.get(
    path="/client/{client_id}",
    description="Get client appointments",
    response_model=list[dto.Appointment],
)
async def get_client_appointments(
        client_id: PositiveInt = Path(),
        employee: dto.Employee = Depends(get_employee),
        dao: HolderDao = Depends(dao_provider)
) -> list[dto.Appointment]:
    if await dao.client.get_client(
            client_id=client_id,
            employee_id=employee.id,
            branch_id=employee.branch.id
    ) is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Client not found",
        )
    return await dao.appointment.get_client_all(
        client_id=client_id,
        branch_id=employee.branch.id,
        employee_id=employee.id
    )


@router.get(
    path="/{appointment_id}",
    description="Get appointment",
    response_model=dto.Appointment
)
async def get_appointment(
        appointment_id: PositiveInt = Path(),
        employee: dto.Employee = Depends(get_employee),
        dao: HolderDao = Depends(dao_provider)
) -> dto.Appointment:
    appointment = await dao.appointment.get_one(
        appointment_id=appointment_id,
        branch_id=employee.branch.id,
        employee_id=employee.id
    )
    if appointment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Appointment not found",
        )
    return appointment


@router.put(
    path="/{appointment_id}",
    description="Update appointment",
    response_model=dto.Appointment,
)
async def update_appointment(
        appointment: schems.Appointment,
        appointment_id: PositiveInt = Path(),
        employee: dto.Employee = Depends(get_employee),
        dao: HolderDao = Depends(dao_provider)
) -> dto.Appointment:
    current_appointment = await dao.appointment.get_one(
        appointment_id=appointment_id,
        branch_id=employee.branch.id,
        employee_id=employee.id
    )
    if current_appointment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Appointment not found",
        )
    return await dao.appointment.update_appointment(
        employee_id=employee.id,
        branch_id=employee.branch.id,
        appointment_id=appointment_id,
        appointment=appointment,
    )


@router.put(
    path="/{appointment_id}/status",
    description="Client early arrival",
    response_model=dto.Appointment,
)
async def change_status(
        appointment_id: PositiveInt = Path(),
        status: dto.AppointmentStatus = Query(),
        employee: dto.Employee = Depends(get_employee),
        dao: HolderDao = Depends(dao_provider)
) -> dto.Appointment:
    return await dao.appointment.update_appointment_status(
        appointment_id=appointment_id,
        employee_id=employee.id,
        branch_id=employee.branch.id,
        status=status
    )


@router.delete(
    path="/{appointment_id}",
    description="Delete appointment",
)
async def delete_appointment(
        appointment_id: PositiveInt = Path(),
        employee: dto.Employee = Depends(get_employee),
        dao: HolderDao = Depends(dao_provider)
):
    appointment = await dao.appointment.get_one(
        appointment_id=appointment_id,
        branch_id=employee.branch.id,
        employee_id=employee.id
    )
    if appointment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Appointment not found",
        )
    await dao.appointment.delete_appointment(
        client_id=appointment.client_id,
        branch_id=employee.branch.id,
        employee_id=employee.id,
        appointment_id=appointment_id,
    )
