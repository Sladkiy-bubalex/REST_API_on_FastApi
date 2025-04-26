import jwt
from functions.functions_server import get_user_by_nickname
from models import User
from schema import TokenData
from config import ALGORITHM, PG_DSN, SECRET_KEY
from sqlalchemy.ext.asyncio import (
    create_async_engine, async_sessionmaker, AsyncSession
)
from typing import Annotated, AsyncGenerator
from fastapi import Depends
from auth import oauth2_scheme
from errors import credentials_exception, expiration_exception


engine = create_async_engine(PG_DSN)
Session = async_sessionmaker(bind=engine, expire_on_commit=False)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with Session() as session:
        yield session


SessionDependancy = Annotated[
    AsyncSession, Depends(get_session, use_cache=True)
]


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)], session: SessionDependancy
) -> User:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        nickname = payload.get("nickname")
        if nickname is None:
            raise credentials_exception
        token_data = TokenData(nickname=nickname)
    except jwt.InvalidTokenError:
        raise credentials_exception
    except jwt.ExpiredSignatureError:
        raise expiration_exception
    user = await get_user_by_nickname(session, token_data.nickname)
    if user is None:
        raise credentials_exception
    if user.role == "admin":
        return user
    return user


AccessDependancy = Annotated[User, Depends(get_current_user)]
