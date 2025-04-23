from fastapi_filter.contrib.sqlalchemy import Filter
from typing import Optional
from models import Advertisement
from decimal import Decimal


class AdvertisementFilter(Filter):
    title: Optional[str] = None
    description: Optional[str] = None
    price: Optional[Decimal] = None

    class Constants(Filter.Constants):
        model = Advertisement
        search_model_fields = ["title", "description", "price"]