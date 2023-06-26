from aiogram.types import BotCommand, BotCommandScopeDefault
from aiogram import Bot


async def set_commands(bot: Bot):
    commands = [
        BotCommand(
            command='start',
            description='Запустить бота'

        ),
        BotCommand(
            command='settings',
            description='Настройки'
        ),
        BotCommand(
            command='help',
            description='Помощь'
        )
    ]
    await bot.set_my_commands(commands=commands, scope=BotCommandScopeDefault())


async def set_description():
    ...
