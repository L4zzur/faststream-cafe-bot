from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from bot.api import create_order, get_menu
from bot.keyboards.product import get_cart_keyboard
from bot.states import ShopState
from shared.logger import setup_logger
from shared.schemas import OrderCreate, OrderItem

logger = setup_logger("bot.handlers.order")

router = Router()


@router.callback_query(F.data == "cart")
async def view_cart(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    user_cart = data.get("cart", {})

    if not user_cart:
        await callback.answer("Корзина пуста!", show_alert=True)
        return

    await state.set_state(ShopState.cart)

    menu_items = await get_menu()
    items_map = {i.code: i for i in menu_items}

    order_text = "🛒 **Ваша корзина:**\n"
    total_price = 0
    order_payload = []

    for code, amount in user_cart.items():
        item = items_map.get(code)
        if item:
            line_price = item.price * amount
            total_price += line_price
            order_text += (
                f"• {item.name}: {amount} шт. x {item.price}₽ = {line_price}₽\n"
            )

            order_payload.append(
                OrderItem(
                    code=code,
                    name=item.name,
                    price=item.price,
                    amount=amount,
                    cooking_time=item.cooking_time,
                )
            )

    order_text += f"**Итого: {total_price}₽**"

    await state.update_data(order_payload=order_payload)

    await callback.message.edit_text(
        order_text, reply_markup=get_cart_keyboard(), parse_mode="Markdown"
    )


@router.callback_query(ShopState.cart, F.data == "checkout")
async def checkout(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    order_payload = data.get("order_payload")

    if not order_payload:
        await callback.answer("Ошибка корзины", show_alert=True)
        return

    try:
        order_create = OrderCreate(user_id=callback.from_user.id, items=order_payload)
        order = await create_order(order_create)

        await state.update_data(cart={}, order_payload=None)
        await state.set_state(ShopState.menu)

        await callback.message.edit_text(
            f"✅ **Заказ `{order.id}` принят!**\n\nОжидайте подтверждения начала готовки от кухни...",
            parse_mode="Markdown",
        )
    except Exception as e:
        logger.error(f"Checkout error: {e}")
        await callback.answer("Ошибка оформления заказа", show_alert=True)
