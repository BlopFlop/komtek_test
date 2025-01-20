from fastapi_users import schemas


class UserRead(schemas.BaseUser[int]):
    """Базовая схема для чтения пользователя."""

    pass


class UserCreate(schemas.BaseUserCreate):
    """Базовая схема для создания пользователя."""

    pass


class UserUpdate(schemas.BaseUserUpdate):
    """Базовая схема для обновления пользователя."""

    pass
