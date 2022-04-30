from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from config import value
from database import db_select_buyers, db_select_product, db_select_item, db_select_admins


async def profile():
    profile_menu = InlineKeyboardMarkup(row_width=1)
    profile_menu.add(
        InlineKeyboardButton('📘 Мои заказы', callback_data='ORDERS'),
        InlineKeyboardButton('Активировать купон', callback_data='COUPON'),
        InlineKeyboardButton('Пополнить баланс', callback_data='TOPUP')
    )
    return profile_menu


async def topup_way(sum):
    topup_menu = InlineKeyboardMarkup(row_width=2)
    topup_menu.add(
        InlineKeyboardButton('BTC', callback_data=f'INSERT_BTC_{sum}'),
        InlineKeyboardButton('QIWI', callback_data=f'INSERT_QIWI_{sum}')
    )
    return topup_menu


async def payment_info(url, bill_id):
    menu = InlineKeyboardMarkup()
    menu.add(
        InlineKeyboardButton('Оплатить', url=url),
        InlineKeyboardButton('Проверить', callback_data=f'QWERT_{bill_id}')
    )
    return menu


async def buyers_list(user, back=None):
    markup = InlineKeyboardMarkup(row_width=2)
    db_buyers = db_select_buyers(user)
    if back:
        markup.add(InlineKeyboardButton('Назад', callback_data='ORDERS'))
        return markup
    markup.add(*[InlineKeyboardButton(db_buyers[a][2], callback_data=f'PURCHASED_{db_buyers[a][4]}') for a in
                 range(len(db_buyers))])
    markup.add(InlineKeyboardButton('Назад', callback_data='BACK_PROFILE'))
    return markup


async def all_product(id, cat_id, admin):
    markup = InlineKeyboardMarkup(row_width=2)
    products = db_select_product(id)
    markup.add(*[InlineKeyboardButton(f'{product[2]} - {product[4]}{value}',
                                      callback_data=f'PRODUCT:{product[0]}') for product in products if
                 admin or len(db_select_item(product[0]))])
    markup.add(InlineKeyboardButton('Назад', callback_data=f'ID_CATALOG_{cat_id}'))
    return markup


async def count_buy(product_id):
    markup = InlineKeyboardMarkup(row_width=3)
    button_1 = InlineKeyboardButton('1', callback_data=f'BUY:1:{product_id}')
    button_2 = InlineKeyboardButton('2', callback_data=f'BUY:2:{product_id}')
    button_3 = InlineKeyboardButton('3', callback_data=f'BUY:3:{product_id}')
    button_4 = InlineKeyboardButton('4', callback_data=f'BUY:4:{product_id}')
    button_5 = InlineKeyboardButton('5', callback_data=f'BUY:5:{product_id}')
    button_6 = InlineKeyboardButton('6', callback_data=f'BUY:6:{product_id}')
    markup.add(InlineKeyboardButton('Выберите количество', callback_data='CHOOSE_COUNT'))
    markup.add(button_1, button_2, button_3, button_4, button_5, button_6)
    return markup


async def check_pay(price, amount, address_id):
    markup = InlineKeyboardMarkup(row_width=2)
    button_1 = InlineKeyboardButton('Проверить платеж', callback_data=f'CHECK_PAY:{price}:{amount}:{address_id}')
    markup.add(button_1)
    return markup
