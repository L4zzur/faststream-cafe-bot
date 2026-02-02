from faststream.rabbit import RabbitQueue, RabbitRouter

from bot.api import create_order, get_menu
from bot.bot import bot as notify_bot
from bot.core.broker import broker
from bot.keyboards.menu import get_menu_keyboard
from shared.schemas import OrderProcessed, OrderStarted
from shared.topics import OrderEvents, OrdersExchange, Queues

router = RabbitRouter()


@router.subscriber(
    RabbitQueue(Queues.BOT_NOTIFICATIONS + "_started", routing_key=OrderEvents.STARTED),
    exchange=OrdersExchange,
)
async def notify_order_started(message: OrderStarted):
    items_text = ""
    for item in message.items:
        items_text += f"• {item.name}: {item.amount} шт.\n"

    await notify_bot.send_message(
        chat_id=message.user_id,
        text=(
            f"👨‍🍳 **Кухня приняла ваш заказ!**\n\n"
            f"🆔: `{message.id}`\n"
            f"🍽️ Содержимое:\n{items_text}\n"
            f"⏳ Расчетное время готовки: **⁓{message.estimated_time} сек.**"
        ),
    )


@router.subscriber(
    RabbitQueue(
        Queues.BOT_NOTIFICATIONS + "_processed", routing_key=OrderEvents.PROCESSED
    ),
    exchange=OrdersExchange,
)
async def notify_order_ready(message: OrderProcessed):
    items_str = ", ".join([f"{i.name} {i.amount} шт." for i in message.items])
    await notify_bot.send_message(
        chat_id=message.user_id,
        text=(
            f"🔔 **Заказ `{message.id}` готов!**\n\n"
            f"🍽 {items_str}\n\n"
            f"Приятного аппетита! ❤️"
        ),
    )
