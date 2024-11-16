from fastapi import APIRouter, Depends, Path, Body, HTTPException, status
from pydantic import PositiveInt

from app import dto
from app.api import schems
from app.api.dependencies import dao_provider, get_superuser
from app.infrastructure.database import HolderDao

router = APIRouter(prefix="/branch", dependencies=[Depends(get_superuser)])


@router.post(path="/", description="Create a branch", response_model=dto.Branch)
async def create_branch(
    branch: schems.Branch, dao: HolderDao = Depends(dao_provider)
) -> dto.Branch:
    existing_branch = await dao.branch.get_by_name(name=branch.name)
    if existing_branch is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Branch already exists"
        )
    return await dao.branch.create(branch=branch)


@router.get(path="/", description="Get branches", response_model=list[dto.Branch])
async def get_branches(dao: HolderDao = Depends(dao_provider)) -> list[dto.Branch]:
    return await dao.branch.get_all()


@router.get(
    path="/{branch_id}",
    description="Get a branch",
    response_model=dto.Branch,
)
async def get_branch(
    branch_id: PositiveInt = Path(), dao: HolderDao = Depends(dao_provider)
) -> dto.Branch:
    existing_branch = await dao.branch.get_branch(branch_id=branch_id)
    if existing_branch is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Branch does not exist"
        )
    return existing_branch


@router.put(
    path="/{branch_id}",
    description="Update a branch",
    response_model=dto.Branch,
)
async def update_branch(
    branch_id: PositiveInt = Path(),
    branch: schems.Branch = Body(),
    dao: HolderDao = Depends(dao_provider),
) -> dto.Branch:
    existing_branch = await dao.branch.get_branch(branch_id=branch_id)
    if existing_branch is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Branch does not exist"
        )
    return await dao.branch.update_branch(branch_id=branch_id, branch=branch)


@router.delete(path="/{branch_id}", description="Delete a branch")
async def delete_branch(
    branch_id: PositiveInt = Path(), dao: HolderDao = Depends(dao_provider)
):
    existing_branch = await dao.branch.get_branch(branch_id=branch_id)
    if existing_branch is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Branch does not exist"
        )
    return await dao.branch.delete_branch(branch_id=branch_id)
