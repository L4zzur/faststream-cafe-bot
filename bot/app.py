import asyncio

from faststream import FastStream

from bot.bot import dp, telegram_bot
from bot.core.broker import broker
from bot.handlers.notify import router as notify_router
from shared.logger import setup_logger

logger = setup_logger("app")


app = FastStream(broker)
broker.include_router(notify_router)


@app.after_startup
async def start_bot():
    logger.info("Starting Telegram polling...")
    asyncio.create_task(dp.start_polling(telegram_bot))
