from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from shared.schemas import Item


def get_product_keyboard(item_code: str, amount: int = 1) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    # +/- Row
    builder.row(
        InlineKeyboardButton(text="➖", callback_data=f"dec:{item_code}"),
        InlineKeyboardButton(text=f"{amount} шт.", callback_data="noop"),
        InlineKeyboardButton(text="➕", callback_data=f"inc:{item_code}"),
    )

    # Actions Row
    builder.row(
        InlineKeyboardButton(text="🔙 Меню", callback_data="menu"),
        InlineKeyboardButton(text="🛒 В корзину", callback_data=f"add:{item_code}"),
    )

    return builder.as_markup()


def get_cart_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="✅ Оформить заказ", callback_data="checkout")
    )
    builder.row(InlineKeyboardButton(text="🔙 Меню", callback_data="menu"))
    return builder.as_markup()
