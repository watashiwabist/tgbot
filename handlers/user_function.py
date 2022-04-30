# -*- coding: UTF-8 -*-
import asyncio
import datetime
import time

import requests
from aiogram.types import CallbackQuery
from forex_python.bitcoin import BtcConverter
from pyqiwip2p import QiwiP2P

from loader import dp, bot
from config import value, cover_img, def_img
from database import db_select_buyers, db_select_subcatalog, db_select_product, db_select_catalog_sub, db_user_info, \
    db_select_buy_item, db_select_item, db_insert_buyers, db_select_buyer, \
    db_delete_item, db_user_insert, db_user_update, db_delete_coupon, db_update_history_admin, top_up_insert, \
    db_select_client
from keyboards import buyers_list, subcatalog_list, all_product, accept_buy_or, count_buy, check_pay, profile, cancel, \
    db_select_coupon, db_select_admins, topup_way, payment_info
from misc.misc import admin_msg, username, time_pay, cur_transfer, coinbase_client, get_LTC_USD
from states import settUser
from aiogram import types
from aiogram.dispatcher import FSMContext


# CALLBACK HANDLER

@dp.callback_query_handler(text_startswith='COUPON')
async def user_activate_coupon(call: CallbackQuery):
    await call.message.answer('Введите купон:')
    await settUser.coupon.set()


@dp.callback_query_handler(text_startswith='ID_CATALOG_')
async def user_view_cat(call: CallbackQuery):
    id_cat = call.data[11:]
    if db_select_subcatalog(cat_id=id_cat):
        try:
            subcatalog_key = await subcatalog_list('ID_SUBCATALOG', id_cat, call.message.chat.id, 'user')
            if len(subcatalog_key.inline_keyboard) == 1:
                await call.answer('Подкаталог пуст')
            else:
                await bot.edit_message_caption(call.message.chat.id, call.message.message_id,
                                               caption='Выберите подкаталог:',
                                               reply_markup=subcatalog_key)
        except Exception as e:
            print(e)
    else:
        await call.answer('Подкаталог пуст')


@dp.callback_query_handler(text_startswith='ID_SUBCATALOG_')
async def user_view_subcat(call: CallbackQuery):
    data = call.data[14:].split('_')
    if db_select_product(data[1]):
        admin = db_select_admins(call.message.chat.id)
        await bot.edit_message_caption(call.message.chat.id, call.message.message_id,
                                       caption='Выберите товар:',
                                       reply_markup=await all_product(data[1], data[0], admin))
    else:
        await call.answer('Раздел пустой')


@dp.callback_query_handler(text_startswith='BACK_SUBCATALOG_')
async def user_view_back_subcat(call: CallbackQuery):
    data = call.data[16:].split('_')
    if db_select_product(data[1]):
        admin = db_select_admins(call.message.chat.id)
        await bot.delete_message(call.message.chat.id, call.message.message_id)
        await bot.send_photo(call.message.chat.id, open(cover_img, 'rb'), caption='Выберите товар',
                             reply_markup=await all_product(data[1], data[0], admin))
    else:
        await call.answer('Произошла ошибка')


@dp.callback_query_handler(text_startswith='PRODUCT:')
async def user_view_pos(call: CallbackQuery):
    product_id = call.data[8:]
    data = db_select_product(id=product_id)
    subcatalog = db_select_subcatalog(subcat_id=data[1])
    catalog = db_select_catalog_sub(subcatalog[1])
    item = db_select_item(product_id)
    await bot.delete_message(call.message.chat.id, call.message.message_id)
    if data[5] == 'None':
        photo = open(def_img, 'rb')
    else:
        photo = data[5]
    await bot.send_photo(call.message.chat.id, photo, f'`{subcatalog[2].upper()}` ➖ *{data[2].upper()}*\n\n'
                                                      f'➖➖➖➖➖➖➖➖➖➖➖➖\n'
                                                      f'📂 *Категория:* {catalog[1]}\n'
                                                      f'📃 *Описание:* {data[3]}\n'
                                                      f'💰 *Цена*: {data[4]} {value}\n\n'
                                                      f'🔄 *Количество:* {len(item)} шт.\n'
                                                      f'➖➖➖➖➖➖➖➖➖➖➖➖\n\n'
                                                      f'✅ Подтвердить покупку?',
                         reply_markup=await accept_buy_or(call.message.chat.id, data[0], data[1], catalog[0]))


@dp.callback_query_handler(text_startswith='GO_BUY:')
async def user_go_buy(call: CallbackQuery):
    product_id = call.data[7:]
    await bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id,
                                        reply_markup=await count_buy(product_id))


@dp.callback_query_handler(text_startswith='CHOOSE_COUNT:')
async def user_choose_count(call: CallbackQuery):
    await call.answer('Псс. Эта кнопка - просто текст')


@dp.callback_query_handler(text_startswith='BUY:')
async def user_buy(call: CallbackQuery):
    await bot.delete_message(call.message.chat.id, call.message.message_id)
    time.sleep(1)
    user = db_user_info(call.message.chat.id)
    try:
        count, product_id = call.data[4:].split(':')
        count = int(count)
        item = db_select_item(product_id)
        product = db_select_product(id=product_id)
        if len(item) < count:
            await call.answer('Нету требуемого количества')
            return
        if user[3]:
            price_prod = int(product[4] - user[3]) * count
            db_user_insert(user=call.message.chat.id, coup=0)
        else:
            price_prod = product[4] * count
        if float(user[4]) >= float(price_prod):
            data_for_user = db_select_buy_item(product_id, count)
            db_user_update(price_prod, call.message.chat.id)
            for a in range(count):
                db_insert_buyers(call.message.chat.id, call.message.chat.username, product[2],
                                 product[0], str(datetime.datetime.today().strftime("%d.%m.%Y %H:%M")),
                                 product[4], str(data_for_user[a][0]), product[3])
            data_text = ''
            subcatalog = db_select_subcatalog(subcat_id=product[1])
            for a in range(len(data_for_user)):
                db_update_history_admin(data_for_user[a][0])
                db_delete_item(data_for_user[a][0])
                data_text = data_text + '*' + str(a + 1) + '*' + '.' + ' ' + str(data_for_user[a][2]) + '\n\n'
                buyer = username(
                    call.message.chat.username) if call.message.chat.username is not None else call.message.chat.first_name
                admin_info = db_user_info(data_for_user[a][3])
                text_for_admin = f'*Новая покупка*\n\n' \
                                 f'*Продукт:* {product[2]}\n' \
                                 f'*Подкаталог:* {subcatalog[2]}\n\n' \
                                 f'*Пользователь:* @{buyer}\n\n' \
                                 f'*Продавец:* {admin_info[1]} | {admin_info[0]}\n\n' \
                                 f'*Данные:*\n\n' \
                                 f'{data_text}'
                await admin_msg(2, text=text_for_admin)
            await call.message.answer(f' *Спасибо* за покупку!\n\n'
                                      f'➖➖➖➖➖➖➖➖➖➖➖➖➖\n'
                                      f'{data_text}'
                                      f'➖➖➖➖➖➖➖➖➖➖➖➖➖')
        else:
            price, address, address_id = await cur_transfer(float(price_prod) - float(user[4]))
            task = asyncio.create_task(time_pay(call.message))
            await call.message.answer(f'Переведите {price} *LTC* на `{address}`\n\n'
                                      f'*Срок действия счета - 50 минут*',
                                      reply_markup=await check_pay(price, int(price_prod) - (user[4]), address_id))
            await task
            await call.answer('Недостаточно средств')
    except TypeError or Exception as e:
        await call.message.answer('Произошла ошибка, введите /start')
        print(f'handlers.user_function.user_accept_buy: {e}')


@dp.callback_query_handler(text_startswith='CHECK_PAY:')
async def user_check_pay(call: CallbackQuery):
    await call.answer('Проверяем платеж')
    time.sleep(2)
    try:
        user_name = f'@{username(call.message.chat.username)}' if call.message.chat.username else call.message.chat.first_name
        check_price, amount, address_id = call.data[10:].split(':')
        client = await coinbase_client()
        user_id = client.get_accounts()[0]['id']
        pay_info = client.get_address_transactions(user_id, address_id).data[0]
        pay_amount = float(pay_info.amount.amount)
        if pay_amount > 0.0:
            if pay_info.status == 'pending':
                new_pay_amount = await get_LTC_USD(pay_amount)
                top_up_insert(call.message.chat.id, new_pay_amount, datetime.datetime.now())
                await bot.delete_message(call.message.chat.id, call.message.message_id)
                db_user_insert(user=call.message.chat.id, amount=amount)
                await call.message.answer(f' *Баланс* успешно пополнен! Можете приступать к покупкам :)\n\n')
                await call.answer(f'*Баланс пополнен на сумму {new_pay_amount} {value} успешно!*')
                text_for_admin = f'*Успешное пополнение*\n\n' \
                                 f'*Сумма:* {pay_amount} LTC || {new_pay_amount} {value}\n\n' \
                                 f'*Покупатель:* {user_name}\n' \
                                 f'*ID покупателя:* {call.message.chat.id}'
                await admin_msg(2, text=text_for_admin)
            else:
                await call.answer('Платеж не найден, попробуйте еще раз')
    except Exception as e:
        await call.message.answer('Произошла ошибка, введите /start')
        print(f'handlers.user_function.user_check_pay: {e}')


@dp.callback_query_handler(text='ORDERS')
async def user_view_pos(call: CallbackQuery):
    if not db_select_buyers(call.message.chat.id):
        await call.answer('У вас еще не было покупок')
    else:
        await bot.edit_message_text('Выберите товар:', call.message.chat.id, call.message.message_id,
                                    reply_markup=await buyers_list(user=call.message.chat.id))
        return


@dp.callback_query_handler(text_startswith='PURCHASED_')
async def user_view_order(call: CallbackQuery):
    try:
        date = call.data[10:]
        data = db_select_buyer(date, call.message.chat.id)
        await bot.edit_message_text(f'*Дата покупки:* {data[4]}\n'
                                    f'*Цена:* {data[5]} {value}\n'
                                    f'*Описание:* {data[7]}\n'
                                    f'➖➖➖➖➖➖➖➖➖➖➖➖\n'
                                    f'{data[6]}',
                                    call.message.chat.id, call.message.message_id,
                                    reply_markup=await buyers_list(call.message.chat.id, True))
    except Exception as e:
        await call.answer('Произошла ошибка, обратитесь в тех.поддержку')
        print(f'handlers.user_function.user_view_order: {e}')


@dp.callback_query_handler(text_startswith='BACK_PROFILE')
async def user_view_order(call: CallbackQuery):
    user = db_user_info(call.message.chat.id)
    coupon_text = ''
    if not user:
        await bot.send_message(call.message.chat.id, 'Пожалуйста, введите /start')
        return
    if user[3] > 0:
        coupon_text = f'\n🎁 *Активный купон:* {user[3]} ₽\n'
    await bot.edit_message_text(f'*👤 Профиль:* {user[1]}\n'
                                f'{coupon_text}'
                                f'\n*✨ Регистрация:* {user[2]}', call.message.chat.id, call.message.message_id,
                                reply_markup=await profile())


def get_btc_price(sum):
    b = BtcConverter()
    price = b.convert_to_btc(sum, 'RUB')
    return price


def qiwi_create_bill(priv_key, sum):
    p2p = QiwiP2P(auth_key=priv_key)
    new_bill = p2p.bill(amount=sum, lifetime=30)
    return new_bill


@dp.callback_query_handler(text_startswith='INSERT')
async def user_insert(call: CallbackQuery):
    sum = int(call.data.split('_')[-1])
    client_info = db_select_client()
    if 'QIWI' in call.data:
        try:
            if client_info[1] == 'token':
                raise Exception
            bill = qiwi_create_bill(client_info[1], sum)
            await bot.send_message(call.message.chat.id, f'*Сумма:* `{sum} RUB`\n\n'
                                                         f'*Для оплаты нажмите на кнопку* - `Оплатить`\n\n'
                                                         f'*После оплаты нажмите на кнопку* - `Проверить оплату`\n\n',
                                   reply_markup=await payment_info(bill.pay_url, bill.bill_id))
        except Exception as e:
            await call.message.answer('В данный момент выбранный способ пополнения недоступен')
            return
    elif 'BTC' in call.data:
        try:
            if client_info[0] == 'login':
                raise Exception
            btc_wallet = client_info[0]
            btc_price = get_btc_price(sum)
            await call.message.answer(f'Пополните кошелек *{btc_wallet}* на сумму {btc_price} *BTC*\n\n'
                                      f'Средства поступят автоматически')
        except:
            await call.message.answer('В данный момент выбранный способ пополнения недоступен')
            return


@dp.callback_query_handler(text_startswith='TOPUP')
async def user_top_up(call: CallbackQuery):
    await call.message.answer('Отправьте сумму для пополнения в *₽*', reply_markup=await cancel())
    await settUser.topUp.set()


# MESSAGE HANDLER
@dp.message_handler(state=settUser.topUp)
async def add_product_price(msg: types.Message, state: FSMContext):
    if not msg.text.isdigit():
        await msg.answer('Отправьте сумму для пополнения в *₽*', reply_markup=await cancel())
        return
    if int(msg.text) < 300:
        await msg.answer('*Минимальная сумма к пополнению 300 ₽*', reply_markup=await cancel())
        return
    await state.update_data(amount=msg.text)
    await state.finish()
    await msg.answer('Выберите способ пополнения', reply_markup=await topup_way(msg.text))
    # try:
    #     price, address, address_id = await cur_transfer(msg.text)
    #     await bot.delete_message(msg.chat.id, msg.message_id)
    #     task = asyncio.create_task(time_pay(msg))
    #     await msg.answer(f'Переведите {price} *LTC* на `{address}`\n\n'
    #                      f'*Срок действия счета - 50 минут*',
    #                      reply_markup=await check_pay(price, msg.text, address_id))
    #     await task
    # except Exception as e:
    #     await state.finish()
    #     print(f'handlers.user_function.add_product_price: {e}')


@dp.message_handler(state=settUser.coupon)
async def activate_coupon(msg: types.Message, state: FSMContext):
    coup = db_select_coupon(text=msg.text)
    if coup is None:
        await msg.answer('Купон неверный')
    else:
        db_user_insert(user=msg.chat.id, coup=coup[2])
        db_delete_coupon(coup[0])
        await msg.answer('Купон активирован')
    await state.finish()
