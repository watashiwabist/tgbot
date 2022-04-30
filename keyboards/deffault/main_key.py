from aiogram.types import ReplyKeyboardMarkup

from config import button_profile, button_catalog, button_help, button_sale, button_work, \
    button_faq
from database import db_select_admins


async def main_start(user):
    menu = ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    menu.add(button_catalog, button_profile)
    menu.add(button_sale)
    menu.add(button_help, button_work, button_faq)
    get_admin = db_select_admins(user)
    if get_admin:
        if get_admin[1] == 2:
            menu.add('Настройка продуктов', 'Сделать рассылку', 'Настройка каталога',
                     'Купоны', 'Сменить API')
    return menu
