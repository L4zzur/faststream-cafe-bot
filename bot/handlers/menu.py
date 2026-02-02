from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from bot.api import create_order, get_menu
from bot.keyboards.menu import get_menu_keyboard
from bot.keyboards.product import get_cart_keyboard, get_product_keyboard
from bot.states import ShopState
from shared.logger import setup_logger
from shared.schemas import OrderCreate, OrderItem

logger = setup_logger("bot.handlers.menu")

router = Router()


@router.callback_query(F.data == "menu")
async def show_menu(callback: CallbackQuery, state: FSMContext):
    await state.set_state(ShopState.menu)
    items = await get_menu()

    data = await state.get_data()
    user_cart = data.get("cart", {})

    cart_lines = []
    total_price = 0

    if user_cart:
        cart_lines.append("🛒 **Ваша корзина:**")
        for code, amount in user_cart.items():
            item = next((i for i in items if i.code == code), None)
            if item:
                price = item.price * amount
                total_price += price
                cart_lines.append(f"• {item.name}: {amount} x {item.price}₽ = {price}₽")

        cart_lines.append(f"**Итого: {total_price}₽**")
        cart_text = "\n".join(cart_lines) + "\n\n"
    else:
        cart_text = "🛒 Корзина пуста\n\n"

    await callback.message.edit_text(
        f"👋 **Async Cafe Меню**\n\n{cart_text}Выберите товар:",
        reply_markup=get_menu_keyboard(items),
        parse_mode="Markdown",
    )


@router.callback_query(F.data.startswith("buy:"))
async def view_item(callback: CallbackQuery, state: FSMContext):
    item_code = callback.data.split(":")[1]

    menu = await get_menu()
    item = next((i for i in menu if i.code == item_code), None)

    if not item:
        await callback.answer("Товар не найден")
        return

    await state.set_state(ShopState.viewing_item)
    await state.update_data(
        current_item_code=item_code, current_item_name=item.name, amount=1
    )

    await callback.message.edit_text(
        f"🍽 **{item.name}**\n\n"
        f"Цена: {item.price}₽\n"
        f"Готовка: ~{item.cooking_time} сек.\n\n"
        f"Выберите количество:",
        reply_markup=get_product_keyboard(item_code, 1),
        parse_mode="Markdown",
    )


@router.callback_query(
    ShopState.viewing_item, F.data.startswith("inc:") | F.data.startswith("dec:")
)
async def change_amount(callback: CallbackQuery, state: FSMContext):
    action, item_code = callback.data.split(":")
    data = await state.get_data()

    current_amount = data.get("amount", 1)

    if action == "inc":
        current_amount += 1
    elif action == "dec":
        current_amount = max(1, current_amount - 1)

    await state.update_data(amount=current_amount)

    # Just update the keyboard, text stays same
    await callback.message.edit_reply_markup(
        reply_markup=get_product_keyboard(item_code, current_amount)
    )


@router.callback_query(ShopState.viewing_item, F.data.startswith("add:"))
async def add_to_cart(callback: CallbackQuery, state: FSMContext):
    item_code = callback.data.split(":")[1]
    data = await state.get_data()
    amount = data.get("amount", 1)
    item_name = data.get("current_item_name", "Товар")

    current_cart = data.get("cart", {})
    new_cart = current_cart.copy()

    current_item_amount = new_cart.get(item_code, 0)
    new_cart[item_code] = current_item_amount + amount

    await state.update_data(cart=new_cart)

    await callback.answer(f"Добавлено {amount} шт. {item_name} в корзину!")
    await show_menu(callback, state)
