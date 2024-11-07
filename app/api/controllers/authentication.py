from typing import Optional

from fastapi import APIRouter, Depends, Response, Cookie, HTTPException, status

from app import dto
from app.api import schems
from app.api.dependencies import dao_provider, AuthProvider, get_settings
from app.config import Settings
from app.infrastructure.database.dao.holder import HolderDao

router = APIRouter()


@router.post(
    path="/superuser/login",
    description="Login superuser",
    response_model=dto.Token,
    tags=["Superuser Authentication"],
)
async def login_superuser(
        response: Response,
        credentials: schems.LoginSuperuser,
        dao: HolderDao = Depends(dao_provider),
        settings: Settings = Depends(get_settings),
) -> dto.Token:
    auth = AuthProvider(settings=settings)
    superuser = await auth.authenticate_superuser(
        credentials.username,
        credentials.password,
        dao
    )
    token = auth.create_token_pairs(sub=superuser.username)
    auth.set_refresh_cookie(response=response, refresh_token=token.refresh_token)
    return token


@router.post(
    path="/employee/login",
    description="Login employee",
    response_model=dto.Token,
    tags=["Employee Authentication"],
)
async def login_employee(
        response: Response,
        credentials: schems.LoginEmployee,
        dao: HolderDao = Depends(dao_provider),
        settings: Settings = Depends(get_settings),
) -> dto.Token:
    auth = AuthProvider(settings=settings)
    employee = await auth.authenticate_employee(
        credentials.email,
        credentials.password,
        dao
    )
    token = auth.create_token_pairs(sub=employee.email)
    auth.set_refresh_cookie(response=response, refresh_token=token.refresh_token)
    return token


@router.post(
    path="/refresh",
    description="Refresh access token",
    response_model=dto.Token,
    tags=["Token Management"],
)
async def refresh_current_token(
        response: Response,
        refresh_token: Optional[str] = Cookie(None, alias="refreshToken"),
        dao: HolderDao = Depends(dao_provider),
        settings: Settings = Depends(get_settings),
) -> dto.Token:
    auth = AuthProvider(settings=settings)
    if not refresh_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token missing",
            headers={"WWW-Authenticate": "Bearer"},
        )
    new_token = await auth.refresh_access_token(
        refresh_token=refresh_token,
        dao=dao
    )
    auth.set_refresh_cookie(response=response, refresh_token=new_token.refresh_token)
    return new_token
