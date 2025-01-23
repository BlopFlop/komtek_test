import logging
from typing import Any, AsyncGenerator, Optional, Union

from fastapi import Depends, Request
from fastapi_users import (
    BaseUserManager,
    FastAPIUsers,
    IntegerIDMixin,
    InvalidPasswordException,
)
from fastapi_users.authentication import (
    AuthenticationBackend,
    BearerTransport,
    JWTStrategy,
)
from fastapi_users.password import PasswordHelper
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from pwdlib import PasswordHash
from pwdlib.hashers.argon2 import Argon2Hasher
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import settings
from core.db import get_async_session
from models.user import User
from schemas.user import UserCreate


async def get_user_db(
    session: AsyncSession = Depends(get_async_session),
) -> AsyncGenerator[SQLAlchemyUserDatabase[User, Any], None]:
    """Async generarot user in db."""
    yield SQLAlchemyUserDatabase(session, User)


bearer_transport = BearerTransport(tokenUrl="auth/jwt/login")


def get_jwt_strategy() -> JWTStrategy:
    """JWT strategy."""
    return JWTStrategy(secret=settings.secret, lifetime_seconds=3600)


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)


class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
    """User manager for current project."""

    async def validate_password(
        self,
        password: str,
        user: Union[UserCreate, User],
    ) -> None | Exception:
        """Validate user password."""
        if len(password) < 3:
            raise InvalidPasswordException(
                reason="Пароль должен содержать, как минимум, 3 символа."
            )
        if user.email in password:
            raise InvalidPasswordException(
                reason="Пароль не может содержать e-mail."
            )

    async def on_after_register(
        self, user: User, request: Optional[Request] = None
    ) -> None:
        """Message about registrage."""
        logging.info(f"Пользователь {user.email} зарегистрирован.")


password_hash = PasswordHash((Argon2Hasher(),))
password_helper = PasswordHelper(password_hash)


async def get_user_manager(
    user_db=Depends(get_user_db),
) -> AsyncGenerator[UserManager, Any]:
    """Get user manager."""
    yield UserManager(user_db, password_helper)


fastapi_users = FastAPIUsers[User, int](get_user_manager, [auth_backend])

current_user = fastapi_users.current_user(active=True)
current_superuser = fastapi_users.current_user(active=True, superuser=True)
