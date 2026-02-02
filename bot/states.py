from aiogram.fsm.state import State, StatesGroup


class ShopState(StatesGroup):
    menu = State()  # Viewing the main menu
    viewing_item = State()  # Viewing a specific item (adjusting quantity)
    cart = State()  # Viewing cart before checkout
