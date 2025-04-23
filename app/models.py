from decimal import Decimal
from datetime import datetime
from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.ext.asyncio import AsyncAttrs


class Base(DeclarativeBase, AsyncAttrs):
    __abstract__ = True

    id: Mapped[int] = mapped_column(primary_key=True)

    @property
    def id_json(self):
        return {"id": self.id}


# class User(Base):
#     __tablename__ = "Users"

#     email: Mapped[str] = mapped_column(unique=True, nullable=True)
#     password: Mapped[str] = mapped_column(nullable=True)
#     is_admin: Mapped[bool] = mapped_column(default=False)
#     advertisement: Mapped[int] = relationship()


class Advertisement(Base):
    __tablename__ = "Advertisements"

    title: Mapped[str] = mapped_column(nullable=True)
    description: Mapped[str]
    price: Mapped[Decimal] = mapped_column(nullable=True)
    # user_id: Mapped[int] = mapped_column(ForeignKey("Users.id"))
    create_at: Mapped[datetime] = mapped_column(server_default=func.now())

    @property
    def json(self):
        return {
            "id": self.id,
            "title": self.title,
            "price": self.price,
            "description": self.description,
            # "user_id": self.user_id,
            "create_at": self.create_at,
        }


ORM_OBJ = Advertisement
ORM_CLS = type [Advertisement]
