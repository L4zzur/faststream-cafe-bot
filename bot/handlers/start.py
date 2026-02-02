from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from bot.api import get_menu
from bot.keyboards.menu import get_menu_keyboard
from bot.states import ShopState
from shared.logger import setup_logger

logger = setup_logger("bot.handlers.start")
router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await state.set_state(ShopState.menu)
    await state.update_data(cart={}, order_payload=None)
    logger.info(f"User {message.from_user.id} sent /start")

    try:
        menu_items = await get_menu()
        welcome_text = (
            "👋 **Добро пожаловать в FastStream Cafe!** 🚀\n\n"
            "Мы готовим самый быстрый код и самый вкусный кофе.\n"
            "Выберите, чем хотите перекусить:\n"
        )
        await message.answer(
            welcome_text,
            reply_markup=get_menu_keyboard(menu_items),
        )
    except Exception as e:
        logger.error(f"Error fetching menu: {e}")
        await message.answer("❌ Меню временно недоступно. Попробуйте позже.")
