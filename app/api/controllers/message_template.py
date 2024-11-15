from fastapi import APIRouter, Path, Depends, HTTPException, status
from pydantic import PositiveInt

from app import dto
from app.api import schems
from app.api.dependencies import dao_provider, get_employee, get_superuser
from app.infrastructure.database import HolderDao

router = APIRouter(prefix="/message-template")


@router.get(
    path="/",
    description="Get all message templates",
    response_model=list[dto.MessageTemplate],
)
async def get_all(
    employee: dto.Employee = Depends(get_employee),
    dao: HolderDao = Depends(dao_provider),
) -> list[dto.MessageTemplate]:
    return await dao.message_template.get_all_by_branch(branch_id=employee.branch.id)


# @router.get(
#     path="/all",
#     description="Get all message templates",
#     response_model=list[dto.MessageTemplate],
# )
# async def get_all(
#         dao: HolderDao = Depends(dao_provider),
# ) -> list[dto.MessageTemplate]:
#     return await dao.message_template.get_all()


# @router.get(
#     path="/branch/{branch_id}",
#     description="Get all message templates by branch",
#     response_model=list[dto.MessageTemplate],
# )
# async def get_all_by_branch(
#         branch_id: PositiveInt = Path(),
#         dao: HolderDao = Depends(dao_provider),
# ) -> list[dto.MessageTemplate]:
#     return await dao.message_template.get_all_by_branch(branch_id=branch_id)


@router.get(
    path="/{message_template_id}",
    description="Get message template",
    response_model=dto.MessageTemplate,
)
async def get_one(
    employee: dto.Employee = Depends(get_employee),
    message_template_id: PositiveInt = Path(),
    dao: HolderDao = Depends(dao_provider),
) -> dto.MessageTemplate:
    message_template = await dao.message_template.get_one(
        message_template_id=message_template_id, branch_id=employee.branch.id
    )
    if message_template is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Message template not found"
        )
    return message_template


@router.post(
    path="/",
    description="Create message template",
    response_model=dto.MessageTemplate,
    dependencies=[Depends(get_superuser)],
)
async def create(
    message_template: schems.MessageTemplate,
    dao: HolderDao = Depends(dao_provider),
) -> dto.MessageTemplate:
    return await dao.message_template.create(
        message_template=message_template, branch_id=message_template.branch_id
    )


@router.put(
    path="/{message_template_id}",
    description="Update message template",
    response_model=dto.MessageTemplate,
    dependencies=[Depends(get_superuser)],
)
async def update_template(
    message_template: schems.MessageTemplate,
    message_template_id: PositiveInt = Path(),
    dao: HolderDao = Depends(dao_provider),
) -> dto.MessageTemplate:
    msg_template = await dao.message_template.get_one(
        message_template_id=message_template_id, branch_id=message_template.branch_id
    )
    if msg_template is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Message template not found"
        )
    return await dao.message_template.update_message_template(
        message_template=message_template,
        message_template_id=message_template_id,
        branch_id=message_template.branch_id,
    )


@router.delete(
    path="/",
    description="Delete message template",
    dependencies=[Depends(get_superuser)],
)
async def delete_template(
    message_template: schems.DeleteMessageTemplate = Path(),
    dao: HolderDao = Depends(dao_provider),
) -> None:
    msg_template = await dao.message_template.get_one(
        message_template_id=message_template.message_template_id,
        branch_id=message_template.branch_id,
    )
    if msg_template is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Message template not found"
        )
    return await dao.message_template.delete_message_template(
        branch_id=message_template.branch_id,
        message_template_id=message_template.message_template_id,
    )
