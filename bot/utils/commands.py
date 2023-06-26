from aiogram.types import BotCommand, BotCommandScopeDefault, BotCommandScopeChat
from aiogram import Bot


async def set_commands(bot: Bot, admin: int = None):
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
        ),
        BotCommand(
            command='add_olimpiad',
            description="Добавить олимпиаду"
        ),
        BotCommand(
            command='show_olimpiads',
            description='Посмотреть все доступные олипиады'
        )
    ]

    await bot.set_my_commands(commands=commands, scope=BotCommandScopeDefault())
