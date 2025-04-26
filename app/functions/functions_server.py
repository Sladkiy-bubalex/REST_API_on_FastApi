from sqlalchemy import select
from models import ORM_CLS, ORM_OBJ, User
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException


async def add_item(session: AsyncSession, item: ORM_OBJ):
    session.add(item)
    try:
        await session.commit()
    except IntegrityError:
        raise HTTPException(409, "Item already exists")


async def get_item_by_id(
        session: AsyncSession,
        orm_cls: ORM_CLS,
        item_id: int
):
    orm_obj = await session.get(orm_cls, item_id)
    if orm_obj is None:
        raise HTTPException(404, "Item not found")
    return orm_obj


async def delete_obj(session: AsyncSession, item_obj: ORM_OBJ):
    await session.delete(item_obj)
    await session.commit()


async def get_user_by_nickname(session: AsyncSession, nickname: str) -> User:
    query = select(User).filter(User.nickname == nickname)
    orm_obj = await session.scalar(query)
    return orm_obj
