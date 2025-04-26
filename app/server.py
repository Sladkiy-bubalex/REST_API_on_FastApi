from fastapi import FastAPI
from errors import login_exception, access_exception
from sqlalchemy import select
from auth import create_access_token, get_password_hash, verify_password
from schema import (
    CreateAdvertisementRequest,
    CreateAdvertisementResponse,
    UpdateAdvertisementRequest,
    UpdateAdvertisementResponse,
    GetAdvertisementResponse,
    DeleteAdvertisementResponse,
    SearchAdvertisementResponse,
    LoginResponse,
    LoginRequest,
    CreateUserRequest,
    CreateUserResponse,
    GetUserResponse,
    UpdateUserResponse,
    UpdateUserRequest,
    DeleteUserResponse,
)
from dependencies import SessionDependancy, AccessDependancy
from functions.functions_server import (
    add_item,
    get_item_by_id,
    delete_obj,
    get_user_by_nickname,
)
from models import Advertisement, User
from config import SUCCESS_REPONSE
from filters import AdvertisementFilter
from fastapi_filter import FilterDepends


app = FastAPI(title="API purchase/sale service")

TAG_ADV = "Аdvertisement"
TAG_AUTH = "Аuthorization"
TAG_USER = "User"


@app.post(
    "/api/v1/advertisement/",
    tags=[TAG_ADV],
    response_model=CreateAdvertisementResponse
)
async def create_advertisement(
    advertisement_data: CreateAdvertisementRequest,
    session: SessionDependancy,
    user: AccessDependancy,
):
    adv_data = advertisement_data.model_dump(exclude_unset=True)
    adv_data["user_id"] = user.id
    adv = Advertisement(**adv_data)
    await add_item(session, adv)
    return adv.id_json


@app.patch(
    "/api/v1/advertisement/{advertisement_id}",
    tags=[TAG_ADV],
    response_model=UpdateAdvertisementResponse,
)
async def update_advertisement(
    advertisement_id: int,
    advertisement_data: UpdateAdvertisementRequest,
    session: SessionDependancy,
    user: AccessDependancy,
):
    adv_data = advertisement_data.model_dump(exclude_unset=True)
    adv_obj = await get_item_by_id(session, Advertisement, advertisement_id)
    if user.id == adv_obj.user_id:
        for field, value in adv_data.items():
            setattr(adv_obj, field, value)
        await add_item(session, adv_obj)
        return adv_obj.json
    raise access_exception


@app.get(
    "/api/v1/advertisement/{advertisement_id}",
    tags=[TAG_ADV],
    response_model=GetAdvertisementResponse,
)
async def get_advertisement(advertisement_id: int, session: SessionDependancy):
    adv_obj = await get_item_by_id(session, Advertisement, advertisement_id)
    return adv_obj.json


@app.delete(
    "/api/v1/advertisement/{advertisement_id}",
    tags=[TAG_ADV],
    response_model=DeleteAdvertisementResponse,
)
async def delete_advertisement(
    advertisement_id: int, session: SessionDependancy, user: AccessDependancy
):
    adv_obj = await get_item_by_id(session, Advertisement, advertisement_id)
    if user.id == adv_obj.user_id:
        await delete_obj(session, adv_obj)
        return SUCCESS_REPONSE
    raise access_exception


@app.get(
    "/api/v1/advertisement/",
    tags=[TAG_ADV],
    response_model=SearchAdvertisementResponse
)
async def search_advertisement(
    session: SessionDependancy,
    filters: AdvertisementFilter = FilterDepends(AdvertisementFilter),
):
    query = select(Advertisement)
    query = filters.filter(query)
    items = await session.scalars(query)
    return {"results": [adv.json for adv in items]}


@app.post("/api/v1/user/", tags=[TAG_USER], response_model=CreateUserResponse)
async def create_user(reg_data: CreateUserRequest, session: SessionDependancy):
    data = reg_data.model_dump(exclude_unset=True)
    hash_password = get_password_hash(data["password"])
    new_user = User(nickname=data["nickname"], password=hash_password)
    token = create_access_token(new_user)
    await add_item(session, new_user)
    return {"id": new_user.id, "token": token}


@app.get(
        "/api/v1/user/{user_id}",
        tags=[TAG_USER],
        response_model=GetUserResponse
)
async def get_user(user_id: int, session: SessionDependancy):
    user_obj = await get_item_by_id(session, User, user_id)
    return user_obj.user_json


@app.patch(
        "/api/v1/user/{user_id}",
        tags=[TAG_USER],
        response_model=UpdateUserResponse
)
async def update_user(
    user_id: int,
    user_data: UpdateUserRequest,
    session: SessionDependancy,
    user: AccessDependancy,
):
    data = user_data.model_dump(exclude_unset=True)
    print(data)
    if data.get("password"):
        data["password"] = get_password_hash(data["password"])
    user_obj = await get_item_by_id(session, User, user_id)
    if user.id == user_obj.id:
        for field, value in data.items():
            setattr(user_obj, field, value)
        access_token = create_access_token(user_obj)
        await add_item(session, user_obj)
        return {
            "nickname": user_obj.nickname,
            "role": user_obj.role,
            "new_token": access_token
        }
    raise access_exception


@app.delete(
        "/api/v1/user/{user_id}",
        tags=[TAG_USER],
        response_model=DeleteUserResponse
)
async def delete_user(
    user_id: int, session: SessionDependancy, user: AccessDependancy
):
    user_obj = get_item_by_id(session, User, user_id)
    if user.id == user_obj.id:
        await delete_obj(session, user_obj)
        return SUCCESS_REPONSE
    raise access_exception


@app.post("/api/v1/login/", tags=[TAG_AUTH], response_model=LoginResponse)
async def login(
    login_data: LoginRequest, session: SessionDependancy
):
    data = login_data.model_dump(exclude_unset=True)
    user = await get_user_by_nickname(session, data["nickname"])
    if user is None or not verify_password(
        data.get("password"), user.password
    ):
        raise login_exception
    access_token = create_access_token(user)
    return {"token": access_token}
