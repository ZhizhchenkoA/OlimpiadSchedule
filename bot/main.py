from aiogram import Bot, Dispatcher
from config import BOT_TOKEN, DATABASE, ADMIN_IDS

import asyncio
from routers import basic
import logging

logging.basicConfig(level=logging.DEBUG)


async def main():
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()
    dp.include_router(basic.router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
