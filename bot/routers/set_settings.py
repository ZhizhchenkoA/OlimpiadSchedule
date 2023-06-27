from aiogram import Bot, Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, CommandObject
from aiogram.fsm.context import FSMContext
import datetime

from bot.utils.states import Settings
from config import db
from db.init_db import Interaction, UserTelegram
from bot.keyboards import keyboards

router = Router()


@router.message(Command('settings'))
async def settings(message: Message, state: FSMContext) -> None:
    await state.set_state(Settings.time_zone)
    await message.answer("Выбран режим настройки параметров бота")
    await message.answer("Введите ваш часовой пояс (относительно МСК)", reply_markup=keyboards.time_zone())


@router.callback_query(F.data.startswith('time_zone'))
@router.message(Settings.time_zone)
async def time_zone(message: Message | CallbackQuery, state: FSMContext, bot: Bot) -> None:
    if type(message) is Message:
        text = message.text
    else:
        text = message.data.replace('time_zone', '')

    if text.isdigit() and -12 <= int(text) <= +12:

        await bot.send_message(
            message.from_user.id,
            'Введите время в часах по вашему времени (от 0 до 23), в которое Вам будет удобно получать уведомления')
        await state.update_data(time_zone=text)
        await state.set_state(Settings.suitable_time)
    else:
        await message.answer('Введите корректное число, удовлеворяющее диапазону от -12 до 12')


@router.message(Settings.suitable_time)
async def suitable_time(message: Message, state: FSMContext) -> None:
    if message.text.isdigit() and 0 <= (text := int(message.text)) <= 23:
        await state.update_data(suitable_time=datetime.time(hour=text))
        await state.set_state(Settings.previous_date)
        await message.answer(
            "Введите количество (или выберите из предложенных) дней до начала события, "
            "за которое необходимо отправить первое предупреждение\n"
            "Число не должно превосходить 4", reply_markup=keyboards.prev())

    else:
        await message.answer('Введите корректное число, удовлеворяющее диапазону от 0 до 23')


@router.callback_query(Settings.previous_date, F.data.startswith('prev'))
@router.message(Settings.previous_date)
async def previous_date(message: Message | CallbackQuery, state: FSMContext, bot: Bot) -> None:
    if type(message) is Message:
        text = message.text
    else:
        text = message.data.replace('prev', '')
    if text.isdigit() and 0 <= int(text) <= 4:
        await bot.send_message(
            message.from_user.id,
            "Введите количество напоминаний о событии во время его проведения\n"
            "Уведомления не будут отправляться больше, чем раз в день\n"
            "Для того, чтобы уведомления отправлялись каждый день, введите -1 или нажмите на кнопку ниже",
            reply_markup=keyboards.amount())
        await state.update_data(previous_date=text)
        await state.set_state(Settings.amount)
    else:
        await message.answer('Введите число')


@router.callback_query(Settings.amount)
@router.message(Settings.amount)
async def amount(message: Message | CallbackQuery, state: FSMContext, bot: Bot):
    if type(message) is Message:
        text = message.text
    else:
        text = message.data.replace('amount', '')
    if (text.isdigit() or (text[1:].isdigit() and text[0] == '-')) and \
            -1 <= int(text):
        await bot.send_message(message.from_user.id,
                               """Настройка бота завершена!\nПриятного использования""")
        await state.update_data(amount=text)

        data = await state.get_data()

        if not db.find_user_telegram(message.from_user.id):
            db.create_user_telegram(telegram_id=int(message.from_user.id))

        user: UserTelegram = db.find_user_telegram(message.from_user.id)

        if user.settings is not None and user.settings.user_id:
            db.del_settings(user.settings)

        db.add_settings(user=user, **data)
        print(data)
        await state.clear()

    else:
        await message.answer('Введите число')
