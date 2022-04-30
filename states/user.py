from aiogram.dispatcher.filters.state import State, StatesGroup


class settUser(StatesGroup):
    topUp = State()
    coupon = State()
