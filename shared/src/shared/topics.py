from enum import StrEnum

from faststream.rabbit import ExchangeType, RabbitExchange


class OrderEvents(StrEnum):
    CREATED = "order.created"
    STARTED = "order.started"
    PROCESSED = "order.processed"
    CANCELED = "order.canceled"


class Queues(StrEnum):
    KITCHEN = "kitchen_queue"
    BOT_NOTIFICATIONS = "bot_queue"


OrdersExchange = RabbitExchange(name="orders", type=ExchangeType.TOPIC)
