# -*- coding: UTF-8 -*-
import datetime
import sqlite3

from config import admins, db


def load_database():
    with sqlite3.connect(db) as con:
        cur = con.cursor()
        # Admin table
        try:
            cur.execute('SELECT * FROM admins')
            print('✅ Connection successful 1/10')
        except sqlite3.DatabaseError:
            print(f'Create admins table 1/10\nAdded an administrator with an ID - {admins}')
            cur.execute('CREATE TABLE IF NOT EXISTS admins('
                        'USER_ID INT,'
                        'LEVEL INT)')
            for a in range(len(admins)):
                cur.execute('INSERT INTO admins VALUES(?, ?)', [admins[a], 2])
        # User table
        try:
            cur.execute('SELECT * FROM users')
            print("✅ Connection successful 2/10")
        except sqlite3.DatabaseError:
            cur.execute('CREATE TABLE IF NOT EXISTS users('
                        'ID INT NOT NULL UNIQUE,'
                        'NAME TEXT,'
                        'DATETIME TEXT,'
                        'SALE INT,'
                        'BALANCE FLOAT,'
                        'UNIQUE ("id") ON CONFLICT IGNORE)')
            print("Create users table 2/10")

        # Buyers table
        try:
            cur.execute('SELECT * FROM buyers')
            print("✅ Connection successful 3/10")
        except sqlite3.DatabaseError:
            cur.execute('CREATE TABLE IF NOT EXISTS buyers('
                        'id INTEGER,'
                        'username TEXT,'
                        'product_name TEXT,'
                        'product_id TEXT,'
                        'date TEXT,'
                        'amount INT,'
                        'data TEXT,'
                        'description TEXT)')
            print("Create buyers table 3/10")
        # Catalog table
        try:
            cur.execute('SELECT * FROM catalog')
            print("✅ Connection successful 4/10")
        except sqlite3.DatabaseError:
            cur.execute('CREATE TABLE IF NOT EXISTS catalog('
                        'ID INTEGER PRIMARY KEY AUTOINCREMENT,'
                        'NAME TEXT)')
            print("Create catalog table 4/10")
        # subcatalog table
        try:
            cur.execute('SELECT * FROM subcatalog')
            print("✅ Connection successful 5/10")
        except sqlite3.DatabaseError:
            cur.execute('CREATE TABLE IF NOT EXISTS subcatalog('
                        'ID INTEGER PRIMARY KEY AUTOINCREMENT,'
                        'ID_CAT INT,'
                        'NAME TEXT)')
            print("Create catalog table 5/10")
        # Product table
        try:
            cur.execute('SELECT * FROM product')

            print("✅ Connection successful 6/10")
        except sqlite3.DatabaseError:
            cur.execute('CREATE TABLE IF NOT EXISTS product('
                        'id INTEGER PRIMARY KEY AUTOINCREMENT,'
                        'subCatID INTEGER,'
                        'name TEXT,'
                        'description TEXT,'
                        'price INT,'
                        'url_img TEXT,'
                        'data TEXT,'
                        'price_admin FLOAT)')
            print("Create product table 6/10")
        # item table
        try:
            cur.execute('SELECT * FROM item')
            print("✅ Connection successful 7/10")
        except sqlite3.DatabaseError:
            cur.execute('CREATE TABLE IF NOT EXISTS item('
                        'id INTEGER PRIMARY KEY AUTOINCREMENT,'
                        'id_prod INTEGER,'
                        'data TEXT,'
                        'id_create INTEGER)')
            print("Create item table 7/10")
        # ltc table
        try:
            cur.execute('SELECT * FROM ltc')
            print("✅ Connection successful 8/10")
        except sqlite3.DatabaseError:
            cur.execute('CREATE TABLE IF NOT EXISTS ltc(btc TEXT, qiwi TEXT)')
            print("Create ltc table 8/10")
        row = cur.fetchone()
        if row is None:
            cur.execute('INSERT INTO ltc(btc, qiwi) VALUES(?, ?)', ('login', 'token'))
        # Купон
        try:
            cur.execute('SELECT * FROM coupon')
            print("✅ Connection successful 9/10\n")
        except sqlite3.DatabaseError:
            cur.execute('CREATE TABLE IF NOT EXISTS coupon('
                        'id INTEGER PRIMARY KEY AUTOINCREMENT,'
                        'coup TEXT,'
                        'price INT)')
            print("Create coupon table 9/10\n")
        try:
            cur.execute('SELECT * FROM history_admin')
            print('✅ Connection successful 10/10\n')
        except sqlite3.DatabaseError:
            print('Create history_admin 10/10')
            cur.execute('CREATE TABLE IF NOT EXISTS history_admin('
                        'ADMIN_ID INTEGER,'
                        'ITEM_DATA TEXT,'
                        'SOLD_OUT INTEGER,'
                        'ID INTEGER,'
                        'PRICE FLOAT,'
                        'SUBCATALOG TEXT)')
        try:
            cur.execute('SELECT * FROM top_up')
            print("✅ Connection successful 11/11\n")
        except sqlite3.DatabaseError:
            cur.execute('CREATE TABLE IF NOT EXISTS top_up('
                        'user_id INTEGER,'
                        'amount INTEGER,'
                        'date TEXT)')
    if con:
        con.close()


# Получение юзера по ID
def db_user_info(user):
    with sqlite3.connect(db) as con:
        cur = con.cursor()
        # noinspection PyBroadException
        try:
            row = cur.execute('SELECT * FROM users WHERE id =?', [user]).fetchone()
            return row
        except Exception as e:
            print(f'db_api.db_user_info: {e}')


def db_select_all_user():
    with sqlite3.connect(db) as con:
        cur = con.cursor()
        # noinspection PyBroadException
        try:
            row = cur.execute('SELECT * FROM users').fetchall()
            return row
        except:
            pass


def db_user_reg(msg):
    with sqlite3.connect(db) as con:
        cur = con.cursor()
        try:
            user = [msg.from_user.id, msg.from_user.first_name, datetime.datetime.now().strftime('%Y-%m-%d'), 0, 0]
            cur.execute('INSERT INTO users VALUES(?, ?, ?, ?, ?);', user)
            con.commit()
        except Exception as e:
            print(f'db_api.db_user_reg: {e}')


# Пополнение баланса
def db_user_insert(user=None, amount=None, coup=None):
    with sqlite3.connect(db) as con:
        cur = con.cursor()
        try:
            if coup is not None:
                cur.execute('UPDATE users SET SALE=? WHERE id=?', [coup, user])
            else:
                cur.execute('UPDATE users SET balance=balance+? WHERE id=?', [amount, user])
            con.commit()
        except Exception as e:
            print(f'db_api_db_user_insert: {e}')


# Запись о попоплнение баланса
def top_up_insert(user_id, amount, date):
    with sqlite3.connect(db) as con:
        cur = con.cursor()
        try:
            cur.execute('INSERT INTO top_up VALUES(?, ?, ?)', [user_id, amount, date])
        except Exception as e:
            print(f'db_api.top_up_insert: {e}')


def top_up_select(user_id):
    with sqlite3.connect(db) as con:
        cur = con.cursor()
        try:
            return cur.execute('SELECT * FROM top_up WHERE user_id=?', [user_id]).fetchall()
        except Exception as e:
            print(f'db_api.top_up_selectt: {e}')


# Измениене баланса
def db_user_update(amount, user):
    with sqlite3.connect(db) as con:
        cur = con.cursor()
        try:
            cur.execute('UPDATE users SET BALANCE=BALANCE-? WHERE ID=?', [amount, user])
            con.commit()
        except Exception as e:
            print(f'db_api.db_user_update: {e}')


# Список купивших
def db_select_buyers(user):
    with sqlite3.connect(db) as con:
        cur = con.cursor()
        try:
            row = cur.execute('SELECT * FROM buyers WHERE id=?', (user,)).fetchall()
            return row
        except Exception as e:
            print(f'db_api.db_select_buyers: {e}')


# Получение конкретной записи купивших
def db_select_buyer(date, id):
    with sqlite3.connect(db) as con:
        cur = con.cursor()
        try:
            row = cur.execute('SELECT * FROM buyers WHERE date=? and id=?', [date, id]).fetchone()
            return row
        except Exception as e:
            print(f'db_api.db_select_buyer: {e}')


# Список администраторов
def db_select_admins(user=None):
    with sqlite3.connect(db) as con:
        cur = con.cursor()
        try:
            if user is None:
                row = cur.execute('SELECT * FROM admins').fetchall()
                return row
            else:
                row = cur.execute('SELECT * FROM admins WHERE USER_ID=?', (user,)).fetchone()
            return row
        except Exception as e:
            print(f'db_api.db_select_admins: {e}')


def db_select_id_admins():
    with sqlite3.connect(db) as con:
        cur = con.cursor()
        try:
            row = cur.execute('SELECT * FROM admins WHERE LEVEL=?', [2]).fetchall()
            return row
        except Exception as e:
            print(f'db_api.db_select_id_admins: {e}')


# Добавление администратора
def db_insert_admin(user_id):
    with sqlite3.connect(db) as con:
        cur = con.cursor()
        try:
            cur.execute('INSERT INTO admins(USER_ID, LEVEL) VALUES (?, ?)', [user_id, 1])
        except Exception as e:
            print(f'db_insert_admin: {e}')


# Удаление администратор
def db_delete_admin(user_id):
    with sqlite3.connect(db) as con:
        cur = con.cursor()
        try:
            cur.execute('DELETE FROM admins WHERE USER_ID=?', [user_id])
        except Exception as e:
            print(f'db_api.db_delete_admin: {e}')


# Список каталогов
def db_select_catalog():
    with sqlite3.connect(db) as con:
        cur = con.cursor()
        try:
            row = cur.execute('SELECT * FROM catalog').fetchall()
            return row
        except Exception as e:
            print(f'db_api.db_select_catalog: {e}')


# Получение каталога по подкаталогу
def db_select_catalog_sub(id):
    with sqlite3.connect(db) as con:
        cur = con.cursor()
        try:
            row = cur.execute('SELECT * FROM catalog WHERE ID=?', [id]).fetchone()
            return row
        except Exception as e:
            print(f'db_api.db_select_catalog: {e}')


# Добавление каталога
def db_insert_catalog(name):
    with sqlite3.connect(db) as con:
        cur = con.cursor()
        try:
            cur.execute('INSERT INTO catalog(name) VALUES (?)', [name])
            con.commit()
        except Exception as e:
            print(f'db_api.db_insert_catalog: {e}')


# Удаление каталога
def db_delete_catalog(id):
    with sqlite3.connect(db) as con:
        cur = con.cursor()
        try:
            cur.execute('DELETE FROM catalog WHERE id=?', [id])
            con.commit()
        except Exception as e:
            print(f'db_api.db_delete_catalog: {e}')


# Получение списка подкаталогов
def db_select_subcatalog(cat_id=None, subcat_id=None):
    with sqlite3.connect(db) as con:
        cur = con.cursor()
        try:
            if cat_id is not None:
                row = cur.execute('SELECT * FROM subcatalog WHERE ID_CAT=?', [cat_id]).fetchall()
            elif subcat_id is not None:
                row = cur.execute('SELECT * FROM subcatalog where ID=?', [subcat_id]).fetchone()
            else:
                row = cur.execute('SELECT * FROM subcatalog').fetchall()
            return row
        except Exception as e:
            print(f'db_api.db_select_subcatalog{e}')


# Добавление под каталога
def db_insert_subcatalog(cat_id, name):
    with sqlite3.connect(db) as con:
        cur = con.cursor()
        try:
            cur.execute('INSERT INTO subcatalog(ID_CAT, NAME) VALUES(?, ?)', [cat_id, name])
            con.commit()
        except Exception as e:
            print(f'db_api.db_insert_subcatalog{e}')


# Удаление под каталога
def db_delete_subcatalog(id_cat=None, id=None):
    with sqlite3.connect(db) as con:
        cur = con.cursor()
        try:
            if id_cat is not None:
                cur.execute('DELETE FROM subcatalog WHERE ID_CAT=?', [id_cat])
            else:
                cur.execute('DELETE FROM subcatalog WHERE ID=?', [id])
            con.commit()
        except Exception as e:
            print(f'db_api.db_insert_subcatalog{e}')


# Создание продукта
def db_insert_product(id, name, description, price, url_image, price_admin):
    with sqlite3.connect(db) as con:
        cur = con.cursor()
        try:
            cur.execute('INSERT INTO product(subCatID, name, description, price, url_img, price_admin) '
                        'VALUES(?, ?, ?, ?, ?, ?)', [id, name, description, price, url_image, price_admin])
            con.commit()
        except Exception as e:
            print(f'db_api.db_insert_product: {e}')


# Получение всех продуктов из подкаталога
def db_select_product(sub_cat_id=None, id=None):
    with sqlite3.connect(db) as con:
        cur = con.cursor()
        try:
            if id is None:
                row = cur.execute('SELECT * FROM product WHERE subCatID=?', [sub_cat_id]).fetchall()
                return row
            else:
                row = cur.execute('SELECT * FROM product WHERE id=?', [id]).fetchone()
                return row
        except Exception as e:
            print(f'db_api.db_select_product: {e}')


def db_delete_product(id, subcat_id=None):
    with sqlite3.connect(db) as con:
        cur = con.cursor()
        try:
            if subcat_id is None:
                cur.execute('DELETE FROM product WHERE id=?', [id])
            else:
                cur.execute('DELETE FROM product WHERE subCatID=?', [subcat_id])
            con.commit()
        except Exception as e:
            print(f'db_api.db_delete_product: {e}')


def db_insert_item(id, data, admin_id):
    with sqlite3.connect(db) as con:
        cur = con.cursor()
        try:
            a = cur.execute('INSERT INTO item(id_prod, data, id_create) VALUES (?, ?, ?)', [id, data, admin_id])
            return a.lastrowid
        except Exception as e:
            print(f'db_api.db_insert_item: {e}')


def db_select_item(id, data=None):
    with sqlite3.connect(db) as con:
        cur = con.cursor()
        try:
            if data:
                row = cur.execute('SELECT * FROM item WHERE data=? AND id_prod=?', [data, id]).fetchone()
            else:
                row = cur.execute('SELECT * FROM item WHERE id_prod=?', [id]).fetchall()
            return row
        except Exception as e:
            print(f'db_api.db_select_item: {e}')


def db_del_item(id):
    with sqlite3.connect('db.sqlite') as con:
        cur = con.cursor()
        try:
            cur.execute('DELETE FROM item WHERE id=?', [id])
        except Exception as e:
            print(f'db_api.db_del_item: {e}')


def db_select_buy_item(id, count):
    with sqlite3.connect(db) as con:
        cur = con.cursor()
        try:
            row = cur.execute('SELECT * FROM item WHERE id_prod=? ORDER BY id DESC LIMIT ?', [id, count]).fetchall()
            return row
        except Exception as e:
            print(f'db_api.db_select_buy_item: {e}')


def db_delete_item(data):
    with sqlite3.connect(db) as con:
        cur = con.cursor()
        try:
            cur.execute('DELETE FROM item WHERE id=?', [data])
            con.commit()
        except Exception as e:
            print(f'db_api.db_delete_item: {e}')


def db_insert_buyers(id, username, product_name, product_id, date, amount, data, description):
    with sqlite3.connect(db) as con:
        cur = con.cursor()
        try:
            cur.execute('INSERT INTO buyers(id, username, product_name, product_id, date, amount, data, description) '
                        'VALUES (?, ?, ? , ?, ?, ?, ?, ?)',
                        [id, username, product_name, product_id, date, int(amount), data, description])
            con.commit()
        except Exception as e:
            print(f'db_api.db_insert_buyers: {e}')


def db_select_client():
    with sqlite3.connect(db) as con:
        cur = con.cursor()
        try:
            row = cur.execute('SELECT * FROM ltc').fetchone()
            return row
        except Exception as e:
            print(f'db_api.db_select_client: {e}')


def db_insert_client(token):
    with sqlite3.connect(db) as con:
        cur = con.cursor()
        try:
            cur.execute('UPDATE ltc SET btc=?, qiwi=?', token)
        except Exception as e:
            print(f'db_api.db_insert_client: {e}')


def db_insert_coupon(coup, price):
    with sqlite3.connect('db.sqlite') as con:
        cur = con.cursor()
        try:
            cur.execute('INSERT INTO coupon(coup, price) VALUES(?, ?)', [coup, price])
        except Exception as e:
            print(f'db_api.db_insert_coupon: {e}')


def db_select_coupon(text=None):
    with sqlite3.connect('db.sqlite') as con:
        cur = con.cursor()
        try:
            if text is None:
                row = cur.execute('SELECT * FROM coupon').fetchall()
            else:
                row = cur.execute('SELECT * FROM coupon WHERE coup=?', [text]).fetchone()
            return row
        except Exception as e:
            print(f'db_api.db_select_coupon: {e}')


def db_delete_coupon(id):
    with sqlite3.connect(db) as con:
        cur = con.cursor()
        try:
            cur.execute('DELETE FROM coupon WHERE id=?', [id])
        except Exception as e:
            print(f'db_api.db_delete_coupon: {e}')


def db_insert_history_admin(admin_id, data, id, price, subcatalog):
    with sqlite3.connect(db) as con:
        cur = con.cursor()
        try:
            cur.execute('INSERT INTO history_admin VALUES(?, ?, ?, ?, ?, ?)',
                        [admin_id, data, 0, id, price, subcatalog])
        except Exception as e:
            print(f'db_api.db_insert_history_admin: {e}')


def db_update_history_admin(id):
    with sqlite3.connect(db) as con:
        cur = con.cursor()
        try:
            cur.execute('UPDATE history_admin SET SOLD_OUT=? WHERE ID=?', [1, id])
        except Exception as e:
            print(f'db_api:db_update_history_admin: {e}')


def db_select_history_admin(admin_id):
    with sqlite3.connect(db) as con:
        cur = con.cursor()
        try:
            row = cur.execute('SELECT * FROM history_admin WHERE ADMIN_ID=?', [admin_id]).fetchall()
            return row
        except Exception as e:
            print(f'dp_api.db_select_history_admin: {e}')


def db_delete_history_admin(id):
    with sqlite3.connect(db) as con:
        cur = con.cursor()
        try:
            cur.execute('DELETE FROM history_admin WHERE ID=?', [id])
        except Exception as e:
            print(f'd_api.db_delete_history_admin: {e}')
