from datetime import timedelta, datetime

import pytz
from fastapi import Depends, HTTPException, status, Response
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from passlib.context import CryptContext

from app import dto
from app.api.dependencies.database import dao_provider
from app.config import Settings
from app.infrastructure.database.dao.holder import HolderDao

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


def get_employee(token: str = Depends(oauth2_scheme)) -> dto.Employee:
    raise NotImplementedError


def get_superuser(token: str = Depends(oauth2_scheme)) -> dto.Superuser:
    raise NotImplementedError


class AuthProvider:

    def __init__(self, settings: Settings):
        self.settings = settings
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        self.secret_key = settings.api.secret
        self.algorythm = "HS256"
        self.access_token_expire = timedelta(minutes=30)
        self.refresh_token_expire = timedelta(days=30)
        self.cookie_domain = "api.example.com"

    def verify_password(
        self,
        plain_password: str,
        hashed_password: str,
    ) -> bool:
        return self.pwd_context.verify(
            plain_password,
            hashed_password,
        )

    def get_password_hash(self, password: str) -> str:
        return self.pwd_context.hash(password)

    async def authenticate_superuser(
        self, username: str, password: str, dao: HolderDao
    ) -> dto.Superuser:
        http_status_401 = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
        superuser = await dao.superuser.get_superuser(
            username=username, with_password=True
        )
        if superuser is None:
            raise http_status_401
        if not self.verify_password(
            password,
            superuser.password,
        ):
            raise http_status_401
        return superuser

    async def authenticate_employee(
        self, email: str, password: str, dao: HolderDao
    ) -> dto.Employee:
        http_status_401 = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
        employee = await dao.employee.get_employee(email=email, with_password=True)
        if employee is None:
            raise http_status_401
        if not self.verify_password(
            password,
            employee.password,
        ):
            raise http_status_401
        return employee

    def create_token(
        self,
        data: dict,
        expires_delta: timedelta,
    ) -> str:
        to_encode = data.copy()
        expire = datetime.now(tz=pytz.timezone("Asia/Tashkent")) + expires_delta
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(
            to_encode,
            self.secret_key,
            algorithm=self.algorythm,
        )
        return encoded_jwt

    def create_tokens(
        self,
        access_token_payload: dict,
        refresh_token_payload: dict,
        access_expires_delta: timedelta,
        refresh_expires_delta: timedelta,
    ) -> dto.Token:
        access_token = self.create_token(
            data=access_token_payload, expires_delta=access_expires_delta
        )
        refresh_token = self.create_token(
            data=refresh_token_payload, expires_delta=refresh_expires_delta
        )
        return dto.Token(
            access_token=access_token,
            refresh_token=refresh_token,
            type="bearer",
            expires_at=self.access_token_expire.total_seconds() * 1000,
        )

    def create_token_pairs(self, sub: str) -> dto.Token:
        return self.create_tokens(
            access_token_payload={"sub": sub},
            refresh_token_payload={"sub": sub},
            access_expires_delta=self.access_token_expire,
            refresh_expires_delta=self.refresh_token_expire,
        )

    async def get_current_superuser(
        self,
        token: str = Depends(oauth2_scheme),
        dao: HolderDao = Depends(dao_provider),
    ) -> dto.Superuser:
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(
                token,
                self.secret_key,
                algorithms=[self.algorythm],
            )
            username: str = payload.get("sub")
            if username is None:
                raise credentials_exception
        except JWTError:
            raise credentials_exception
        superuser = await dao.superuser.get_superuser(username=username)
        if superuser is None:
            raise credentials_exception
        return superuser

    async def get_current_employee(
        self,
        token: str = Depends(oauth2_scheme),
        dao: HolderDao = Depends(dao_provider),
    ) -> dto.Employee:
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(
                token,
                self.secret_key,
                algorithms=[self.algorythm],
            )
            email: str = payload.get("sub")
            if email is None:
                raise credentials_exception
        except JWTError:
            raise credentials_exception
        employee = await dao.employee.get_employee(email=email)
        if employee is None:
            raise credentials_exception
        return employee

    async def refresh_access_token(
        self, refresh_token: str, dao: HolderDao = Depends(dao_provider)
    ) -> dto.Token:
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate refresh token",
            headers={"WWW-Authenticate": "Bearer"},
        )

        try:
            payload = jwt.decode(
                refresh_token,
                self.secret_key,
                algorithms=[self.algorythm],
            )
            sub: str = payload.get("sub")
            if sub is None:
                raise credentials_exception
        except JWTError:
            raise credentials_exception

        user = await dao.superuser.get_superuser(username=sub)
        if user is None:
            user = await dao.employee.get_employee(email=sub)
            if user is None:
                raise credentials_exception

        new_access_token_payload = {"sub": sub}
        new_access_token = self.create_token(
            data=new_access_token_payload, expires_delta=self.access_token_expire
        )

        return dto.Token(
            access_token=new_access_token,
            refresh_token=refresh_token,
            type="bearer",
            expires_at=self.access_token_expire.total_seconds() * 1000,
        )

    def set_refresh_cookie(self, response: Response, refresh_token: str) -> None:
        response.set_cookie(
            key="refreshToken",
            value=refresh_token,
            httponly=True,
            secure=True,
            samesite="none",
            domain=self.cookie_domain,
            path="/",
            max_age=int(self.refresh_token_expire.total_seconds()),
        )

    def delete_refresh_cookie(self, response: Response) -> None:
        response.delete_cookie(
            key="refreshToken",
            httponly=True,
            secure=True,
            samesite="none",
            domain=self.cookie_domain,
            path="/",
        )
