import asyncio

from src.bot.bot_instance import dp, bot
from src.handlers import messages_handler, callback_handler

dp.include_router(messages_handler.router)
dp.include_router(callback_handler.router)

async def main() -> None:
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())