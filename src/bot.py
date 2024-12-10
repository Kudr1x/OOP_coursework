import logging

import asyncio

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode

from aiogram.client.default import DefaultBotProperties

from src.config import BOT_TOKEN
from src.handlers import start_handler

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN))
dp = Dispatcher()

dp.include_router(start_handler.router)

async def main() -> None:
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())


