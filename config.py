# - *- coding: utf- 8 - *-


# Введите токен бота
token_bot = '1731229367:AAHDGiGHXjMyb8qpk5xKxoGxEO9ivkANRhU'

# ПРИ ИЗМЕНЕНИЕ ТЕКСТА НЕ УДАЛЯТЬ КОВЫЧКИ!
# ПРИ ИЗМЕНЕНИИ ТЕКСТА ЧТОБЫ НАЧАТЬ С НОВОЙ СТРОКИ ТЕКСТ НУЖНО ДОБАВИТЬ '\n' - БЕЗ КОВЫЧЕК
# ПРИМЕР:
#   start_text = 'Hello\nWorld!'
# ВЫВОД:
#   Hello
#   World!
# ЧТОБЫ ИЗМЕНИТЬ СТИЛЬ НАПИСАНИЯ ТЕКСТА ИСПОЛЬЗУЕМ ТАКИЕ СИМВОЛЫ КАК: `, *
# `Hello World` - на разных устройствах разное отображение, обычно используется для
# быстрого копирование выделнной этими символоами строки
# *Hello World* - жирный шрифт

# Введите ID Админа @getmyid_bot
admins = [211886096, 5305502929, 5303735558]

# Текст после /start
# В последующих обновлениях, это все можно будет изменять через админ. панель
reg_text = '🖖🏿, кто-то!\n' \
           'Приветствую тебя в самом ах%@нном магазе.\n' \
           'Мы открылись недавно, поэтому не забудь заглянуть в акции🥶\n' \
           'Надеюсь, ты найдёшь для себя что-нибудь вкусное🤪\n'
auth_text = 'С возвращением'

# Текст для админов
start_text_adm = 'Приветственный текст для админов'

# Чтобы добавить картинку к сообщению:
# Сохранить фото в корень проекта и добавить название в переменную help_url
# Например help_url = 'defolt.jpg'
help_url = 'image/defolt.jpg'
help_text = 'Если что-то случилось Вы можете написать любому оператору\n\n' \
            '@operator\_banana1\n' \
            '@operator\_banana2\n\n' \
            'Если вопрос о не находе сразу прикрепляйте фото и описание проблемы.\n\n' \
            'Операторы ответят в районе часа.\n\n' \
            'При оскорблении сотрудника магазина бан⛔️'

# Обменники текст
changer_text = 'Тестовый текст'

sale_text = '❗️*Акция* ❗️\n\n' \
            'В честь успешного года работы нашего магазина доступна следующая акция:\n' \
            'При покупке 2 гр любых вкусняшек🤪, в подарок ещё 1 гр.\n\n' \
            'Акция доступна один раз для каждого нового пользователя.\n' \
            'Для активации нужно написать оператору магазина:\n' \
            '@operator\_banana1\n' \
            '@operator\_banana2'

faq_text = '*Дорогой друг, пожалуйста, соблюдай правила!*✌️\n\n' \
           '*Условия покупок:*\n' \
           '*1. Покупая у нас вы автоматически соглашаетесь с правилами сделки.*\n' \
           '*2.Гарантия на адрес составляет 12 часов с момента оплаты товара клиентом. По истечении этого срока претензии по отсутствию товара не принимаются. Время считается от момента совершения покупки до момента получения письма о проблеме.*\n' \
           '*3. Запрещается передавать адрес закладки 3-им лицам.*\n' \
           '*4. Каждая проблема разбирается индивидуально и зависит от каждой конкретной ситуации.*\n' \
           '*5. Решение проблемы зависит исключительно от администарции магазина.*\n' \
           '*6. Без фото, или с фото залитыми на ресурсы не указанные в скобках - проблемы не рассматриваем!*\n' \
           '*7. Оскорбления сотрудников магазина влечет за собой отказ в перезакладе.*\n' \
           '*8. Если у клиента менее 1ух покупок на площадке , проблема рассмотрена не будет.*\n' \
           '*9. Проблема решается в срок от 5 минут до 2 дней - будьте терпеливы и мы обязательно решим Вашу проблему.*\n\n' \
           '*Давайте будем работать честно и все останутся довольны!*'

work_text = 'Мы предлагаем не самые прибыльные, но самые безопасные 🔒 вакансии по сравнению с нашими конкурентами.\n' \
            'Актуальные вакансии: \n' \
            'Курьер \n' \
            'Оператор с опытом работы (от 2х месяцев)\n' \
            'По всем вопросам \n\n' \
            '@operator\_banana1\n\n' \
            '@operator\_banana2\n\n' \
            'Так же возможно сотрудничество с магазином. Цена выставления своих позиций у нас 50 000₽.'

# Обложка магазина
# - написать абсолютный путь до изображения
cover_img = 'image/cover.jpg'
# Если хотите установить одну единственную обложку для товара, сохраните обложку в корень папки и измените
# переменную на вашу
def_img = 'image/cover.jpg'

# Меню
button_profile = '👤 Мой профиль'
button_catalog = '💩 Каталог'
button_help = '🆘 Поддержка'
button_changer = '💰 Пополнить баланс'
button_faq = '❓ Правила'
button_work = '⚙️ Работа'
button_sale = '📍 Акции'

# Текст, если товар в каталоге пуст
product_empty_text = 'Данный каталог пуст'

catalog_info = '`🛒 Выберите категорию товаров:`'
product_info = '`Выберите товар:`'

value = '₽'

db = 'db.sqlite'
