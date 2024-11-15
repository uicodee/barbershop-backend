from fastapi import FastAPI
from .authentication import router as authentication_router
from .employee import router as employee_router
from .branch import router as branch_router
from .message_template import router as message_template_router
from .client import router as client_router
from .appointment import router as appointment_router


def setup(app: FastAPI) -> None:
    app.include_router(router=authentication_router)
    app.include_router(router=employee_router, tags=["Employee"])
    app.include_router(router=branch_router, tags=["Branch"])
    app.include_router(router=message_template_router, tags=["Message Template"])
    app.include_router(router=client_router, tags=["Client"])
    app.include_router(router=appointment_router, tags=["Appointment"])
