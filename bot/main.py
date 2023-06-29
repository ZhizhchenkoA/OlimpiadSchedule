from aiogram import Bot, Dispatcher
from config import BOT_TOKEN, DATABASE, ADMIN_IDS, REDIS_HOST, REDIS_PASSWORD, REDIS_PORT
from utils.commands import set_commands
import asyncio
from routers import basic, set_settings, admin
import logging
from aiogram.fsm.storage.redis import RedisStorage


async def on_startup(bot: Bot):
    await set_commands(bot)


async def on_shutdown(bot: Bot):
    await bot.session.close()


async def main():
    bot = Bot(token=BOT_TOKEN, parse_mode='HTML')
    storage = RedisStorage.from_url(f'redis://root:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}/0')
    dp = Dispatcher(storage=storage)
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)
    dp.include_routers(basic.router, set_settings.router, admin.router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
