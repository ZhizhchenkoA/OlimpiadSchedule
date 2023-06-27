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
    args = command.args
    if not args:
        await help_command(message)

    else:
        await bot.delete_message(message.from_user.id, message.message_id)
        if 'del' in args:
            args = args.replace('del', '')
            olimpiad = db.find_olimpiad_by_id(int(args))
            db.remove_subscription(user, olimpiad)
            await message.answer('Олимпиада успешно удалена из подписок')
        else:
            olimpiad = db.find_olimpiad_by_id(int(args))
            db.add_subscription(user, olimpiad)
            await message.answer("Подписка на олимпиаду успешно оформлена")


@router.message(Command('show_all'))
async def show_olimpiads(message: Message):
    data: list[Olimpiad] = db.select_all(class_=Olimpiad)
    text = ''
    for i in data:
        text += i.name + '\n'
        text += f'<a href="https://t.me/{BOT_NAME}?start={i.id}">подписаться</a>'
        text += '\n'
    await message.answer(text)


@router.message(Command('help'))
async def help_command(message: Message):
    await message.answer("описание бота")


@router.message(Command("show_my"))
async def show_my(message: Message):
    user = db.find_user_telegram(message.from_user.id)
    text = ''
    if user.subscriptions is not None:
        for olimpiad in user.subscriptions:
            text += olimpiad.name + '\n'
            text += f'<a href="https://t.me/{BOT_NAME}?start=del{olimpiad.id}">отписаться</a>' +'\n'
    if text:
        await message.answer(text)
    else:
        await message.answer('В подписках нет ни одной олимиады\n'
                             'Для начала добавьте олимпиаду с помощью /show_all')