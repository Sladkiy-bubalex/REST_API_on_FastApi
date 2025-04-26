from decimal import Decimal
from datetime import datetime
from config import ROLE
from sqlalchemy import ForeignKey, func, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.ext.asyncio import AsyncAttrs


class Base(DeclarativeBase, AsyncAttrs):
    __abstract__ = True

    id: Mapped[int] = mapped_column(primary_key=True)

    @property
    def id_json(self):
        return {"id": self.id}


class Advertisement(Base):
    __tablename__ = "Advertisements"

    title: Mapped[str] = mapped_column(nullable=True)
    description: Mapped[str]
    price: Mapped[Decimal] = mapped_column(nullable=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("Users.id"))
    create_at: Mapped[datetime] = mapped_column(server_default=func.now())
    user: Mapped["User"] = relationship(
        "User", lazy="joined", back_populates="advertisements"
    )

    @property
    def json(self):
        return {
            "id": self.id,
            "title": self.title,
            "price": self.price,
            "description": self.description,
            "user_id": self.user_id,
            "create_at": self.create_at,
        }


class User(Base):
    __tablename__ = "Users"

    nickname: Mapped[str] = mapped_column(unique=True, nullable=True)
    password: Mapped[str] = mapped_column(nullable=True)
    role: Mapped[ROLE] = mapped_column(String, default="user")
    advertisements: Mapped[list["Advertisement"]] = relationship(
        Advertisement, lazy="joined", back_populates="user"
    )

    @property
    def user_json(self):
        return {"id": self.id, "nickname": self.nickname, "role": self.role}


ORM_OBJ = Advertisement | User
ORM_CLS = type[Advertisement] | type[User]
