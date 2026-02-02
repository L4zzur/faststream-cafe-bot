from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from shared.schemas import Item


def get_menu_keyboard(items: list[Item]) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for item in items:
        builder.button(
            text=f"{item.icon} {item.name} - {item.price}₽",
            callback_data=f"buy:{item.code}",
        )
    builder.adjust(2)

    # Bottom row
    builder.row(
        InlineKeyboardButton(text="🛒 Корзина", callback_data="cart"),
        InlineKeyboardButton(text="🔄 Обновить", callback_data="menu"),
    )
    return builder.as_markup()
