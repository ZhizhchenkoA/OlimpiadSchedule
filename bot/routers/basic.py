from aiogram import Router, Bot, F
from aiogram.types import Message
from aiogram.filters import Command, CommandObject
from config import db, BOT_NAME
from db.init_db import Olimpiad

router = Router()


@router.message(Command('start'))
async def start(message: Message, command: CommandObject, bot: Bot):
    user = db.find_user_telegram(message.from_user.id)
    if not user:
        user = db.create_user_telegram(message.from_user.id)
    if user.settings is None:
        return await message.answer('Добрый день!\n'
                                    'Для начала работы с ботом необходима настройка. '
                                    'Нажмите /settings для осуществление настройки бота')
    if not command.args:
        await help_command(message)

    else:
        await bot.delete_message(message.from_user.id, message.message_id)
        olimpiad = db.find_olimpiad_by_id(int(command.args))
        db.add_subscription(user, olimpiad)
        await message.answer("Подписка на олимпиаду успешно оформлена")


@router.message(Command('show_olimpiads'))
async def show_olimpiads(message: Message):
    data: list[Olimpiad] = db.select_all(class_=Olimpiad)
    text = ''
    for i in data:
        text += i.name + '\n'
        text += f'<a href="https://t.me/{BOT_NAME}?start={i.id}">ссылка</a>'
        text += '\n'
    await message.answer(text)


@router.message(Command('help'))
async def help_command(message: Message):
    await message.answer("описание бота")
