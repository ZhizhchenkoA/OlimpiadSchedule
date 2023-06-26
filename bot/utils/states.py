from aiogram.fsm.state import State, StatesGroup


class Settings(StatesGroup):
    time_zone = State()
    suitable_time = State()
    previous_date = State()
    amount = State()


class Admin(StatesGroup):
    add_olimpiad = State()
    add_description = State()
    number_of_stages = State()
    add_stage = State()
    add_stage_description = State()
    add_stage_dates = State()
