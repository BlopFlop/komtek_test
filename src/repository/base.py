from typing import Any, TypeAlias

from fastapi import Depends
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeBase

from core.db import get_async_session
from core.logging_ import async_func_log_msg

DatabaseModel: TypeAlias = DeclarativeBase
SchemaCreate: TypeAlias = BaseModel
SchemaUpdate: TypeAlias = BaseModel
SchemaDB: TypeAlias = BaseModel


class RepositoryBase:
    """Base CRUD operations in current application."""

    def __init__(
        self,
        model: type[DatabaseModel],
        session: AsyncSession = Depends(get_async_session),
    ) -> None:
        self.model = model
        self.session = session

    @async_func_log_msg(
        start_process_msg="Получение одного элемента из бд по id.",
        end_process_msg="Элемент получен.",
    )
    async def get(
        self,
        obj_id: int,
    ) -> SchemaDB:
        """Get one item model for id."""
        db_obj = await self.session.execute(
            select(self.model).where(self.model.id == obj_id)
        )
        return db_obj.scalars().first()

    @async_func_log_msg(
        start_process_msg="Получение всех Элементов из бд.",
        end_process_msg="Элементы получены.",
    )
    async def get_multi(self) -> list[SchemaDB]:
        """Get all items model."""
        db_objs = await self.session.execute(select(self.model))
        return db_objs.scalars().all()

    @async_func_log_msg(
        start_process_msg="Создание элемента в бд.",
        end_process_msg="Элемент создан.",
    )
    async def create(
        self,
        obj_in: SchemaCreate,
    ) -> SchemaDB:
        """Create item model for id."""
        obj_in_data = obj_in.model_dump()
        db_obj = self.model(**obj_in_data)
        self.session.add(db_obj)
        await self.session.commit()
        await self.session.refresh(db_obj)
        return db_obj

    @async_func_log_msg(
        start_process_msg="Обновление элемента в бд.",
        end_process_msg="Элемент обновлен.",
    )
    async def update(
        self,
        db_obj: SchemaDB,
        obj_in: SchemaUpdate,
    ) -> SchemaDB:
        """Update item model for id."""
        obj_data = jsonable_encoder(db_obj)
        update_data = obj_in.model_dump(exclude_unset=True)

        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])

        self.session.add(db_obj)
        await self.session.commit()
        await self.session.refresh(db_obj)
        return db_obj

    @async_func_log_msg(
        start_process_msg="Удаление элемента в бд.",
        end_process_msg="Элемент удален.",
    )
    async def remove(
        self,
        db_obj: SchemaDB,
    ) -> SchemaDB:
        """Delete item model for id."""
        await self.session.delete(db_obj)
        await self.session.commit()
        return db_obj

    @async_func_log_msg(
        start_process_msg=(
            "Получение элемента или списка Элементов"
            " по имени поля и по значению."
        ),
        end_process_msg="Элемент получен.",
    )
    async def get_obj_for_field_arg(
        self, field: str, arg: Any, many: bool
    ) -> SchemaDB | list[SchemaDB]:
        """Get model for keyword argument."""
        db_obj = await self.session.execute(
            select(self.model).where(getattr(self.model, field) == arg)
        )
        if many:
            return db_obj.scalars().all()
        else:
            return db_obj.scalars().first()
