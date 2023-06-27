from aiogram.utils.keyboard import InlineKeyboardBuilder


def time_zone():
    kb = InlineKeyboardBuilder()
    for i in range(-1, 10):
        kb.button(text=str(i) + ' МСК' if i == 0 else str(i), callback_data='time_zone' + str(i))
    kb.adjust(4)
    return kb.as_markup()


def prev():
    kb = InlineKeyboardBuilder()
    for i in range(0, 5):
        kb.button(text=str(i), callback_data='prev' + str(i))
    kb.adjust(4)
    return kb.as_markup()


def amount():
    kb = InlineKeyboardBuilder()
    kb.button(text='Каждый день', callback_data='amount-1')
    return kb.as_markup()
