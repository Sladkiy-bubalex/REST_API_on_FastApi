from fastapi import FastAPI, Query
from typing import Dict, Any

from sqlalchemy import select
from schema import (
    CreateAdvertisementRequest,
    CreateAdvertisementResponse,
    UpdateAdvertisementRequest,
    UpdateAdvertisementResponse,
    GetAdvertisementResponse,
    DeleteAdvertisementResponse,
    SearchAdvertisementResponse
)
from dependencies import SessionDependancy
from functions.functions_server import add_item, get_item_by_id, delete_obj
from models import Advertisement
from config import SUCCESS_REPONSE
from filters import AdvertisementFilter
from fastapi_filter import FilterDepends


app = FastAPI(
    title="API purchase/sale service"
)


@app.post(
        "/api/v1/advertisement/",
        tags=["advertisement"],
        response_model=CreateAdvertisementResponse
)
async def create_advertisement(advertisement_data: CreateAdvertisementRequest, session: SessionDependancy):
    adv_data = advertisement_data.model_dump(exclude_unset=True)
    adv = Advertisement(**adv_data)
    await add_item(session, adv)
    return adv.id_json


@app.patch(
        "/api/v1/advertisement/{advertisement_id}",
        tags=["advertisement"],
        response_model=UpdateAdvertisementResponse
)
async def update_advertisement(
    advertisement_id: int,
    advertisement_data: UpdateAdvertisementRequest,
    session: SessionDependancy
):
    adv_data = advertisement_data.model_dump(exclude_unset=True)
    adv_obj = await get_item_by_id(session, Advertisement, advertisement_id)
    for field, value in adv_data.items():
        setattr(adv_obj, field, value)
    await add_item(session, adv_obj)
    return adv_obj.json


@app.get(
        "/api/v1/advertisement/{advertisement_id}",
        tags=["advertisement"],
        response_model=GetAdvertisementResponse
)
async def get_advertisement(advertisement_id: int, session: SessionDependancy):
    adv_obj = await get_item_by_id(session, Advertisement, advertisement_id)
    return adv_obj.json


@app.delete(
        "/api/v1/advertisement/{advertisement_id}",
        tags=["advertisement"],
        response_model=DeleteAdvertisementResponse
)
async def delete_advertisement(advertisement_id: int, session: SessionDependancy):
    adv_obj = await get_item_by_id(session, Advertisement, advertisement_id)
    await delete_obj(session, adv_obj)
    return SUCCESS_REPONSE


@app.get(
        "/api/v1/advertisement/",
        tags=["advertisement"],
        response_model=SearchAdvertisementResponse
)
async def search_advertisement(
    session: SessionDependancy,
    filters: AdvertisementFilter = FilterDepends(AdvertisementFilter)
):
    query = select(Advertisement)
    query = filters.filter(query)
    items = await session.scalars(query)
    return {"results": [adv.json for adv in items]}