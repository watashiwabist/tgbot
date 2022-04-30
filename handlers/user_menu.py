# - *- coding: utf- 8 - *-
import os

from aiogram import types
from aiogram.types import CallbackQuery

from config import button_profile, button_catalog, catalog_info, button_help, help_url, help_text, cover_img, \
    sale_text, button_sale, faq_text, button_faq, button_work, work_text
from database import db_user_info, db_select_catalog
from keyboards import catalog
from keyboards.inline.user_key import *
from loader import dp, bot


@dp.message_handler(text=button_profile)
async def user_profile(msg: types.Message):
    await bot.delete_message(msg.chat.id, msg.message_id)
    user = db_user_info(msg.chat.id)
    coupon_text = ''
    if not user:
        await bot.send_message(msg.chat.id, 'Пожалуйста, введите /start')
        return
    if user[3] > 0:
        coupon_text = f'\n🎁 *Активный купон:* {user[3]} ₽\n'
    await bot.send_message(msg.chat.id, f'*👤 Профиль:* {user[1]}\n\n'
                                        f'*💰 Баланс:* {user[4]} {value}\n'
                                        f'{coupon_text}'
                                        f'\n*✨ Регистрация:* {user[2]}',
                           reply_markup=await profile())


@dp.message_handler(text=button_catalog)
async def user_catalog(msg: types.Message):
    await bot.delete_message(msg.chat.id, msg.message_id)
    if not db_select_catalog():
        await msg.answer('Каталог пуст')
    else:
        await bot.send_photo(msg.chat.id, open(cover_img, 'rb'), catalog_info,
                             reply_markup=await catalog('ID_CATALOG_', None))


@dp.message_handler(text=button_help)
async def user_help(msg: types.Message):
    check_help_img = os.path.exists(help_url)
    await bot.delete_message(msg.chat.id, msg.message_id)
    if check_help_img:
        help_img = open(help_url, 'rb')
        await bot.send_photo(msg.chat.id, photo=help_img, caption=help_text)
    else:
        await msg.answer(help_text)


@dp.message_handler(text=button_faq)
async def user_changer(msg: types.Message):
    await msg.answer(faq_text)


@dp.message_handler(text=button_work)
async def user_changer(msg: types.Message):
    await msg.answer(work_text)


@dp.message_handler(text=button_sale)
async def user_changer(msg: types.Message):
    await msg.answer(sale_text)


@dp.callback_query_handler(text_startswith='BACK_CATALOG')
async def user_view_pos(call: CallbackQuery):
    if not db_select_catalog():
        await call.answer('Каталог пуст')
    else:
        await bot.edit_message_caption(call.message.chat.id, call.message.message_id, caption=catalog_info,
                                       reply_markup=await catalog('ID_CATALOG_', None))
