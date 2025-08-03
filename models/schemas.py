from pydantic import BaseModel
from datetime import datetime
from typing import Dict


class SpotPrice(BaseModel):
    pair: str
    amount: float


class SpotPriceFromAPI(BaseModel):
    amount: float
    base: str
    currency: str


class SpotPriceResponse(BaseModel):
    data: SpotPriceFromAPI


class PriceTimeline(BaseModel):
    prices: Dict[datetime, SpotPrice]
