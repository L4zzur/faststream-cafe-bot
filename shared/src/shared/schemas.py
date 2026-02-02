import random
import string
from enum import StrEnum

from pydantic import BaseModel, Field


def gen_id() -> str:
    chars = string.ascii_uppercase + string.digits
    return "FS-" + "".join(random.choices(chars, k=6))


class Status(StrEnum):
    CREATED = "created"
    STARTED = "started"
    PROCESSED = "processed"


class Item(BaseModel):
    code: str
    icon: str
    name: str
    price: int
    cooking_time: int


class OrderItem(BaseModel):
    code: str
    name: str
    price: int
    amount: int
    cooking_time: int


class OrderCreate(BaseModel):
    user_id: int
    items: list[OrderItem]


class OrderCreated(BaseModel):
    id: str = Field(default_factory=gen_id)
    user_id: int
    items: list[OrderItem]
    status: Status = Status.CREATED


class OrderStarted(BaseModel):
    id: str
    user_id: int
    items: list[OrderItem]
    estimated_time: int
    status: Status = Status.STARTED


class OrderProcessed(BaseModel):
    id: str
    user_id: int
    items: list[OrderItem]
    status: Status = Status.PROCESSED
