from aiogram import Bot, Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
import datetime
from bot.utils.states import Settings
from config import db
from db.init_db import Interaction, UserTelegram

router = Router()


@router.message(Command('settings'))
async def settings(message: Message, state: FSMContext) -> None:
    await state.set_state(Settings.time_zone)
    await message.answer("Выбран режим настройки параметров бота")
    await message.answer("Введите ваш часовой пояс (относительно МСК)")


@router.message(Settings.time_zone)
async def time_zone(message: Message, state: FSMContext) -> None:
    if message.text.isdigit() and -12 <= (text := int(message.text)) <= +12:
        await message.answer(
            'Введите время в часах по вашему времени (от 0 до 23), в которое Вам будет удобно получать уведомления')
        await state.update_data(time_zone=text)
        await state.set_state(Settings.suitable_time)
    else:
        await message.answer('Введите корректное число, удовлеворяющее диапазону от -12 до 12')


@router.message(Settings.suitable_time)
async def suitable_time(message: Message, state: FSMContext) -> None:
    if message.text.isdigit() and 0 <= (text := int(message.text)) <= 23:
        await message.answer(
            """Введите количество дней до начала события, за которое необходимо отправить первое предупреждение\nЧисло не должно превосходить 4""")
        await state.update_data(suitable_time=datetime.time(hour=text))
        await state.set_state(Settings.previous_date)
    else:
        await message.answer('Введите корректное число, удовлеворяющее диапазону от 0 до 23')


@router.message(Settings.previous_date)
async def previous_date(message: Message, state: FSMContext) -> None:
    if message.text.isdigit() and 0 <= (text := int(message.text)) <= 4:
        await message.answer(
            """Введите количество напоминаний о событии во время его проведения\nУведомления не будут отправляться больше, чем раз в день\nДля того, чтобы уведомления отправлялись каждый день, введите -1""")
        await state.update_data(previous_date=text)
        await state.set_state(Settings.amount)
    else:
        await message.answer('Введите число')


@router.message(Settings.amount)
async def amount(message: Message, state: FSMContext):
    if (message.text.isdigit() or (message.text[1:].isdigit() and message.text[0] == '-')) and \
            -1 <= (text := int(message.text)):
        await message.answer(
            """Настройка бота завершена!\nПриятного использования""")
        await state.update_data(amount=text)
        await state.set_state(Settings.amount)
        data = await state.get_data()

        if not db.find_user_telegram(message.from_user.id):
            db.create_user_telegram(telegram_id=int(message.from_user.id))

        user: UserTelegram = db.find_user_telegram(message.from_user.id)

        if user.settings is not None and user.settings.user_id:
            db.del_settings(user.settings)

        db.add_settings(user=user, **data)

        await state.clear()

    else:
        await message.answer('Введите число')
