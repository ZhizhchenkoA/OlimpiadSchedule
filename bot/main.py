from aiogram import Bot, Dispatcher
from config import BOT_TOKEN, DATABASE, ADMIN_IDS
from utils.commands import set_commands, set_description
import asyncio
from routers import basic, set_settings
import logging


async def on_startup(bot: Bot):
    await set_commands(bot)


async def main():
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()
    dp.startup.register(on_startup)
    dp.include_routers(basic.router, set_settings.router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    asyncio.run(main())
