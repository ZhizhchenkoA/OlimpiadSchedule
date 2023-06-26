from aiogram import Router, Bot, F
from aiogram.types import Message
from aiogram.filters import Command

router = Router()


@router.message(Command('start'))
async def start(message: Message):
    await message.answer('/settings')

# @router.message()
# async def misc(message: Message):
#     await message.answer(message.text)