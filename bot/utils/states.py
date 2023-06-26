from aiogram.fsm.state import State, StatesGroup


class Settings(StatesGroup):
    time_zone = State()
    suitable_time = State()
    previous_date = State()
    amount = State()
