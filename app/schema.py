from pydantic import BaseModel
from decimal import Decimal
from datetime import datetime
from typing import Literal


class SuccessResponse(BaseModel):
    status: Literal["success"]


class CreateAdvertisementRequest(BaseModel):
    title: str
    description: str
    price: Decimal
    # user_id: int


class CreateAdvertisementResponse(BaseModel):
    id: int


class UpdateAdvertisementRequest(BaseModel):
    title: str | None = None
    description: str | None = None
    price: Decimal | None = None
    # user_id: int | None = None
    create_at: datetime | None = None


class UpdateAdvertisementResponse(UpdateAdvertisementRequest):
    pass


class GetAdvertisementResponse(BaseModel):
    id: int
    title: str
    description: str
    price: Decimal
    # user_id: int
    create_at: datetime


class DeleteAdvertisementResponse(SuccessResponse):
    pass


class SearchAdvertisementResponse(BaseModel):
    results: list[GetAdvertisementResponse]