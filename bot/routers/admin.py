import logging
import datetime
import re
from aiogram import Bot, F, Router
from aiogram.types import Message
from aiogram.filters import Command, CommandObject
from aiogram.fsm.context import FSMContext

from config import db, ADMIN_IDS
from bot.utils.states import Admin

router = Router()


@router.message(Command('add_olimpiad'))
async def start_adding(message: Message, state: FSMContext):
    await state.set_state(Admin.add_olimpiad)
    await message.answer("Введите название олимпиады")


@router.message(Admin.add_olimpiad)
async def add_olimpiad(message: Message, state: FSMContext):
    await state.update_data(olimpiad=message.text)
    await state.set_state(Admin.add_description)
    await message.answer("Введите описание олимпиады")


@router.message(Admin.add_description)
async def add_description(message: Message, state: FSMContext):
    await state.update_data(description=message.text)
    await state.set_state(Admin.number_of_stages)
    await message.answer("Введите количество этапов "
                         "(целое число, большее 0)")


@router.message(Admin.number_of_stages)
async def number_of_stages(message: Message, state: FSMContext):
    data = await state.get_data()
    if message.text.isdigit() and int(message.text) > 0 and data.get('number_of_stages') is None:

        await state.update_data(number_of_stages=int(message.text))
        await state.set_state(Admin.add_stage)
        await message.answer("Введите название этапа")
    elif data.get('number_of_stages') is not None:
        await state.set_state(Admin.add_stage)
        await message.answer("Введите название этапа")
    else:
        await message.answer('Введите число')


@router.message(Admin.add_stage)
async def add_stage(message: Message, state: FSMContext):
    await state.update_data(stage=message.text)
    await state.set_state(Admin.add_stage_description)
    await message.answer("Введите опиcание этапа")


@router.message(Admin.add_stage_description)
async def add_stage(message: Message, state: FSMContext):
    await state.update_data(stage_description=message.text)
    await state.set_state(Admin.add_stage_dates)
    await message.answer("Введите даты проведения этапа в формате ДД.ММ.ГГГГ "
                         "(через пробел дату начала и дату окончания)")


@router.message(Admin.add_stage_dates)
async def add_stage(message: Message, state: FSMContext):
    days = message.text.split()
    try:

        beginning_date = datetime.date(year=int(days[0].split('.')[2]), month=int(days[0].split('.')[1]),
                                       day=int(days[0].split('.')[0]))
        ending_date = datetime.date(year=int(days[1].split('.')[2]), month=int(days[1].split('.')[1]),
                                    day=int(days[1].split('.')[0]))
        data = await state.get_data()
        stage = db.add_stage(name=data.get('stage'), description=data.get('stage_description'),
                             beginning_date=beginning_date, ending_date=ending_date)
        if data.get('stages_list') is None:
            await state.update_data(stages_list=[stage])
        else:
            stages = data.get('stages_list')
            stages.append(stage)
            await state.update_data(stage_list=stages)
        number_of_stages = data.get('number_of_stages') - 1
        print(number_of_stages)
        await state.update_data(number_of_stages=number_of_stages)
        data = await state.get_data()
        if number_of_stages == 0:
            db.add_olimpiad(name=data.get('olimpiad'), description=data.get('description'),
                            stages=data.get('stage_list'))
            await state.clear()
            return await message.answer('Олимпиада успешно добавлена')
        else:
            await message.answer("Добавьте новый этап")
            await state.set_state(Admin.add_stage)
    except Exception as err:

        await message.answer("Введите правильный формат данных!")
