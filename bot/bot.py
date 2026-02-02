from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums.parse_mode import ParseMode

from bot.core.config import bot_settings
from shared.logger import setup_logger

from .handlers import setup_message_routers

logger = setup_logger("bot")


bot = Bot(
    token=bot_settings.bot_token,
    default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN),
)
telegram_bot = bot
dp = Dispatcher()
message_routers = setup_message_routers()
dp.include_router(message_routers)
