from aiogram import Bot, Dispatcher
from config import BOT_TOKEN, DATABASE, ADMIN_IDS
from utils.commands import set_commands
import asyncio
from routers import basic, set_settings, admin
import logging


async def on_startup(bot: Bot):
    await set_commands(bot)
    # for i in ADMIN_IDS:
    #     await set_commands(bot, i)


async def on_shutdown(bot: Bot):
    await bot.session.close()


async def main():
    bot = Bot(token=BOT_TOKEN, parse_mode='HTML')
    dp = Dispatcher()
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)
    dp.include_routers(basic.router, set_settings.router, admin.router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
