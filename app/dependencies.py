from config import PG_DSN
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from typing import Annotated, AsyncGenerator
from fastapi import Depends


engine = create_async_engine(PG_DSN)
Session = async_sessionmaker(bind=engine, expire_on_commit=False)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with Session() as session:
        yield session

SessionDependancy = Annotated[AsyncSession, Depends(get_session)]