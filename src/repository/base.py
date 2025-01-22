from typing import TypeAlias, Any

from fastapi import Depends
from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel

from core.db import get_async_session

DatabaseModel: TypeAlias = DeclarativeBase
SchemaCreate: TypeAlias = BaseModel
SchemaUpdate: TypeAlias = BaseModel
SchemaDB: TypeAlias = BaseModel


class RepositoryBase:
    """Base CRUD operations in current application."""

    def __init__(
        self,
        model: type[DatabaseModel],
        session: AsyncSession = Depends(get_async_session)
    ) -> None:
        self.model = model
        self.session = session

    async def get(
        self,
        obj_id: int,
    ) -> SchemaDB:
        """Get one item model for id."""
        db_obj = await self.session.execute(
            select(self.model).where(self.model.id == obj_id)
        )
        return db_obj.scalars().first()

    async def get_multi(self) -> list[SchemaDB]:
        """Get all items model."""
        db_objs = await self.session.execute(select(self.model))
        return db_objs.scalars().all()

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

    async def remove(
        self,
        db_obj: SchemaDB,
    ) -> SchemaDB:
        """Delete item model for id."""
        await self.session.delete(db_obj)
        await self.session.commit()
        return db_obj

    async def get_obj_for_field_arg(
        self,
        field: str,
        arg: Any,
        many: bool
    ) -> SchemaDB | list[SchemaDB]:
        """Get model for keyword argument."""
        db_obj = await self.session.execute(
            select(self.model).where(getattr(self.model, field) == arg)
        )
        if many:
            return db_obj.scalars().all()
        else:
            return db_obj.scalars().first()
