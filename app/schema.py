from pydantic import BaseModel
from decimal import Decimal
from datetime import datetime
from typing import Literal
from config import ROLE


class SuccessResponse(BaseModel):
    status: Literal["success"]


class BaseUserRequest(BaseModel):
    nickname: str
    password: str


class BaseIdResponse(BaseModel):
    id: int


class CreateAdvertisementRequest(BaseModel):
    title: str
    description: str
    price: Decimal


class CreateAdvertisementResponse(BaseIdResponse):
    pass


class UpdateAdvertisementRequest(BaseModel):
    title: str | None = None
    description: str | None = None
    price: Decimal | None = None
    user_id: int | None = None
    create_at: datetime | None = None


class UpdateAdvertisementResponse(UpdateAdvertisementRequest):
    pass


class GetAdvertisementResponse(BaseModel):
    id: int
    title: str
    description: str
    price: Decimal
    user_id: int
    create_at: datetime


class DeleteAdvertisementResponse(SuccessResponse):
    pass


class SearchAdvertisementResponse(BaseModel):
    results: list[GetAdvertisementResponse]


class CreateUserRequest(BaseUserRequest):
    role: ROLE | None = "user"


class CreateUserResponse(BaseIdResponse):
    token: str


class UpdateUserRequest(BaseModel):
    nickname: str | None = None
    password: str | None = None
    role: str | None = None


class UpdateUserResponse(BaseModel):
    nickname: str | None = None
    new_token: str
    role: str | None = None


class GetUserResponse(BaseIdResponse):
    nickname: str
    role: str


class DeleteUserResponse(SuccessResponse):
    pass


class LoginRequest(BaseUserRequest):
    pass


class LoginResponse(BaseModel):
    token: str


class TokenData(BaseModel):
    nickname: str
