from datetime import datetime

from fastapi import APIRouter

from core.broker import broker
from shared.logger import setup_logger
from shared.schemas import OrderCreate, OrderCreated
from shared.topics import OrderEvents, OrdersExchange

logger = setup_logger("order")
router = APIRouter(prefix="/order", tags=["Orders"])


@router.post("")
async def create_order(order: OrderCreate):
    logger.info(f"Received order request from user {order.user_id} for {order.items}")

    event = OrderCreated(**order.model_dump())

    await broker.publish(
        message=event,
        exchange=OrdersExchange,
        routing_key=OrderEvents.CREATED,
    )
    return {
        "msg": "Order accepted for processing",
        "order_time": datetime.now(),
        "data": event,
    }
