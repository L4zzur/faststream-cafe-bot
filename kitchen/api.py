import asyncio
from random import randint

from faststream.rabbit import RabbitQueue
from faststream.rabbit.fastapi import RabbitRouter

from shared.config import settings
from shared.logger import setup_logger
from shared.schemas import OrderCreated, OrderProcessed, OrderStarted, Status
from shared.topics import OrderEvents, OrdersExchange, Queues

logger = setup_logger("kitchen")

router = RabbitRouter(settings.rabbit_url)


@router.subscriber(
    RabbitQueue(Queues.KITCHEN, routing_key=OrderEvents.CREATED),
    exchange=OrdersExchange,
)
@router.publisher(
    exchange=OrdersExchange,
    routing_key=OrderEvents.PROCESSED,
)
async def process_order(message: OrderCreated) -> OrderProcessed:
    logger.info(f"Processing order {message.id} for user {message.user_id}")
    total_time = sum(item.cooking_time * item.amount for item in message.items)
    logger.info(f"Cooking will take {total_time} seconds")

    # Имитация ожидания ответа кухни
    await asyncio.sleep(randint(1, 15))

    await router.broker.publish(
        OrderStarted(
            id=message.id,
            user_id=message.user_id,
            items=message.items,
            estimated_time=total_time,
        ),
        exchange=OrdersExchange,
        routing_key=OrderEvents.STARTED,
    )

    # Имитация времени приготовления
    await asyncio.sleep(total_time)

    result = OrderProcessed(
        id=message.id,
        user_id=message.user_id,
        items=message.items,
        status=Status.PROCESSED,
    )

    logger.info(f"Order {message.id} processed in {total_time} seconds")
    return result
