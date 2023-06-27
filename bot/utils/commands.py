from aiogram.types import BotCommand, BotCommandScopeDefault, BotCommandScopeChatMember
from aiogram import Bot
from config import BOT_ID


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
            command='show_all',
            description='Посмотреть все доступные олимпиады'
        ),

        BotCommand(
            command='add_olimpiad',
            description="Добавить олимпиаду"
        ),
        BotCommand(
            command='show_my',
            description='Посмотреть подписки'
        )
    ]

    await bot.set_my_commands(commands=commands, scope=BotCommandScopeDefault())
