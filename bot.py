from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.types import Message
from aiogram.types.message import ContentTypes

import datetime

import sqlite3

from keyboard_reply import Keyboard_reply

from States_dialog import states
from States_dialog import dialog

from secret import Bot_global_token
from secret import Sberbank_payments_test_token

# Создаем экземпляр бота
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------#
Bot = Bot(token=Bot_global_token)
bot = Dispatcher(Bot, storage=MemoryStorage())

K = Keyboard_reply()
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------#

#Подключаемся к БД
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------#
try:
    sqlite_connection = sqlite3.connect('sqlite_python.db')
    cursor = sqlite_connection.cursor()
    print("Успешно подключились к SQLite")

    sqlite_select_query = "select sqlite_version();"
    cursor.execute(sqlite_select_query)

    record = cursor.fetchall()
    print("Версия базы данных SQLite: ", record)

except sqlite3.Error as error:
    print("Ошибка при подключении к sqlite", error)
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------#


#Обработка Старт
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------#
@bot.message_handler(commands=["start"])
async def start(message: Message):
    cursor.execute("SELECT Stuff_status FROM Stuff WHERE Stuff_id = ?", (message.chat.id, ))
    result = str(cursor.fetchone())
    if result == '(6,)':
        cursor.execute("UPDATE Stuff SET Stuff_state = 0 WHERE Stuff_id = ?", (message.from_user.id, ))
        sqlite_connection.commit()
        await message.answer(dialog.START_TEH_ADMIN, reply_markup=K.reply_keyboard('start_teh_admin_keyboard'))
    elif result == '(5,)':
        cursor.execute("UPDATE Stuff SET Stuff_state = 0 WHERE (Stuff_id = ?", (message.from_user.id, ))
        sqlite_connection.commit()
        await message.answer(dialog.START_ADMIN_PLUS, reply_markup=K.reply_keyboard('start_admin_plus_keyboard'))
    elif result == '(4,)':
        cursor.execute("UPDATE Stuff SET Stuff_state = 0 WHERE (Stuff_id = ?", (message.from_user.id, ))
        sqlite_connection.commit()
        await message.answer(dialog.START_ADMIN, reply_markup=K.reply_keyboard('start_admin_keyboard'))
    elif result == '(3,)':
        cursor.execute("UPDATE Stuff SET Stuff_state = 0 WHERE (Stuff_id = ?", (message.from_user.id, ))
        sqlite_connection.commit()
        await message.answer(dialog.START_KONSULTANT, reply_markup=K.reply_keyboard('start_konsultant_keyboard'))
    else:
        cursor.execute("SELECT * FROM users WHERE user_id = ?", (message.from_user.id, ))
        entry = cursor.fetchone()
        if entry is None:
            cursor.execute("INSERT INTO users VALUES (?, ?, ?, ?)",
                           (message.from_user.id, message.from_user.username, '1', '0'))
            sqlite_connection.commit()
            await message.answer(dialog.START_FIRST_USER, reply_markup=K.reply_keyboard('start_skip_keyboard'))
            await states.S_NAME.set()
        else:
            cursor.execute("SELECT user_nick FROM users WHERE user_id = ?", (message.from_user.id,))
            name = str(cursor.fetchone())[2:][:-3]
            await message.answer(f'Привет, {name}, рад снова тебя видеть тут! Давай посмотрим,'
                                 ' чем могу помочь в этот раз)', reply_markup=K.reply_keyboard('start_katalog_keyboard'))
            await states.S_NAME.set()
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------#


PRICE_cherry_mx = types.LabeledPrice(label='Cherry MX', amount=1200000)


#Имя
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------#
@bot.message_handler(commands=['terms'])
async def process_terms_command(message: types.Message):
    await message.reply('Тут правила', reply=False)


@bot.message_handler(state=states.S_NAME)
async def set_name(message: types.Message, state: FSMContext):
    if message.text != 'Пропустить' and message.text != 'Каталог':
        cursor.execute("UPDATE users SET user_nick = ? WHERE User_id = ?", (message.text, message.from_user.id))
        sqlite_connection.commit()
        await message.answer(f'Добро пожаловать, {message.text}')

    if Sberbank_payments_test_token.split(':')[1] == 'TEST':
        await Bot.send_message(message.chat.id, 'Все, что у нас есть')
    await Bot.send_invoice(
        message.chat.id,
        title='Cherry MX Black',
        description='"Элегантные Кейкапы для CherryMX.\n'
                    'Напечатаны с помощью технологии SLA-печати (лазерной стереолитографии) с лазерной гравировкой,'
                    'Обеспечивающей прозрачность букв и графики."',
        provider_token=Sberbank_payments_test_token,
        currency='rub',
        photo_url='https://www.cherrymx.de/_Resources/Persistent/3'
                  '/6/f/e/36fede38472002e9b9fd7b78b8b4cfcf781e2fca/mobileImage.png',
        photo_height=512,
        photo_width=512,
        photo_size=512,
        is_flexible=False,  # True если конечная цена зависит от способа доставки
        prices=[PRICE_cherry_mx],
        start_parameter='Keycaps',
        payload='some-invoice-payload-for-our-internal-use')
    await state.finish()


@bot.pre_checkout_query_handler(lambda query: True)
async def process_pre_checkout_query(pre_checkout_query: types.PreCheckoutQuery):
    await Bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)


@bot.message_handler(content_types=ContentTypes.SUCCESSFUL_PAYMENT)
async def process_successful_payment(message: types.Message):
    pmnt = message.successful_payment.to_python()

    await Bot.send_message(
        message.chat.id,
        dialog.SUCCESSFUL_PAYMENT.format(
            total_amount=message.successful_payment.total_amount // 100,
            currency=message.successful_payment.currency
        ), reply_markup=K.reply_keyboard('after_purchase_keyboard')
    )

    Data = datetime.datetime.now().strftime('%Y-%m-%d')
    Time = datetime.datetime.now().strftime('%H:%M:%S')

    cursor.execute("INSERT INTO purchases VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                   (pmnt['telegram_payment_charge_id'],
                    pmnt['provider_payment_charge_id'],
                    message.from_user.id,
                    Data,
                    Time,
                    int(int(pmnt['total_amount']) / 100),
                    pmnt['currency'],
                    pmnt['invoice_payload']
                    )
                   )
    sqlite_connection.commit()
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------#


#Обработка Help
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------#
@bot.message_handler(commands=["help"])
async def start(message: Message):
    await message.answer(dialog.HELP)
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------#


#Рассылка
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------#
@bot.message_handler(content_types=['text'], text='Рассылка')
async def spam(message: Message):

    cursor.execute("SELECT Stuff_status FROM Stuff WHERE Stuff_id = ?", (message.from_user.id, ))
    proverka_na_prava = str(cursor.fetchone())

    if proverka_na_prava == '(6,)' or proverka_na_prava == '(5,)' or proverka_na_prava == '(4,)':
        cursor.execute("UPDATE Stuff SET Stuff_state = 1 WHERE Stuff_id = ?", (message.from_user.id, ))
        sqlite_connection.commit()
        await states.spam.set()
        await message.answer(dialog.SPAM_START, reply_markup=K.reply_keyboard('back_action'))


@bot.message_handler(state=states.spam)
async def start_spam(message: Message, state: FSMContext):
    if message.text != 'Назад':
        cursor.execute(f'''SELECT user_id FROM users''')
        spam_base = cursor.fetchall()
        for z in range(len(spam_base)):
            await Bot.send_message(spam_base[z][0], message.text)
            await message.answer(dialog.SPAM_END)
            await state.finish()
    else:
        cursor.execute("UPDATE Stuff SET Stuff_state = 0 WHERE Stuff_id = ?", (message.from_user.id, ))
        sqlite_connection.commit()
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------#


#Ответ на кнопки добавления новых админов
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------#
@bot.message_handler(content_types=['text'], text='Добавить ТехAдмина')
async def Add_Teh_Admin(message: types.Message):

    cursor.execute("SELECT Stuff_status FROM Stuff WHERE Stuff_id = ?", (message.from_user.id, ))
    proverka_na_prava_Teh_Admin = str(cursor.fetchone())

    if proverka_na_prava_Teh_Admin == '(6,)':
        await states.S_ENTER_ID_TEH_Admin.set()
        await message.answer(dialog.NEW_TEH_ADMIN, reply_markup=K.reply_keyboard('back_action'))
    else:
        await message.answer(f"Недостаточно прав {proverka_na_prava_Teh_Admin}")


@bot.message_handler(state=states.S_ENTER_ID_TEH_Admin)
async def S_ENTER_ID_TEH_Admin(message: Message, state: FSMContext):
    if message.text != 'Назад':
        all_for_admin = str(message.text).split('-')
        print(message.text, all_for_admin)
        cursor.execute("INSERT INTO Stuff VALUES (?, ?, ?, ?, ?)",
                       (all_for_admin[0], all_for_admin[1].lstrip(), 6, 0, 0))
        sqlite_connection.commit()

        await message.answer(dialog.NEW_TEH_ADMIN_FINAL)
        await Bot.send_message(all_for_admin[0], dialog.NEW_TEH_ADMIN_FINAL_TO)
        await state.finish()
    else:
        cursor.execute("UPDATE Stuff SET Stuff_state = 0 WHERE Stuff_id = ?", message.from_user.id)
        sqlite_connection.commit()


@bot.message_handler(lambda message: message.text == 'Добавить Aдмина+')
async def Add_Admin_plus(message: types.Message):

    cursor.execute("SELECT Stuff_status FROM Stuff WHERE Stuff_id = ?", message.from_user.id)
    proverka_na_prava_Admin_plus = str(cursor.fetchone())

    if proverka_na_prava_Admin_plus == '(6,)':
        await states.S_ENTER_ID_Admin_plus.set()
        await message.answer(dialog.NEW_ADMIN_PLUS, reply_markup=K.reply_keyboard('back_action'))
    else:
        await message.answer(f"Недостаточно прав {proverka_na_prava_Admin_plus}")


@bot.message_handler(state=states.S_ENTER_ID_Admin_plus)
async def S_ENTER_ID_Admin_plus(message: Message, state: FSMContext):
    if message.text != 'Назад':
        all_for_admin = str(message.text).split('-')
        print(message.text, all_for_admin)
        cursor.execute("INSERT INTO Stuff VALUES (?, ?, ?, ?, ?)",
                       (all_for_admin[0], all_for_admin[1].lstrip(), 5, 0, 0))
        sqlite_connection.commit()

        await message.answer(dialog.NEW_ADMIN_PLUS_FINAL)
        await Bot.send_message(all_for_admin[0], dialog.NEW_ADMIN_PLUS_FINAL_TO)
        await state.finish()
    else:
        cursor.execute("UPDATE Stuff SET Stuff_state = 0 WHERE Stuff_id = ?",
                       message.from_user.id)
        sqlite_connection.commit()


@bot.message_handler(lambda message: message.text == 'Добавить Aдмина')
async def Add_Admin(message: types.Message):

    cursor.execute("SELECT Stuff_status FROM Stuff WHERE Stuff_id = ?",
                   message.from_user.id)
    proverka_na_prava_Admina = str(cursor.fetchone())

    if proverka_na_prava_Admina == '(6,)' or proverka_na_prava_Admina == '(5,)':
        await states.S_ENTER_ID_Admin.set()
        await message.answer(dialog.NEW_ADMIN, reply_markup=K.reply_keyboard('back_action'))
    else:
        await message.answer(f"Недостаточно прав {proverka_na_prava_Admina}")


@bot.message_handler(state=states.S_ENTER_ID_Admin)
async def S_ENTER_ID_Admin(message: Message, state: FSMContext):
    if message.text != 'Назад':
        all_for_admin = str(message.text).split('-')
        print(message.text, all_for_admin)
        cursor.execute("INSERT INTO Stuff VALUES (?, ?, ?, ?, ?)",
                       (all_for_admin[0], all_for_admin[1].lstrip(), 4, 0, 0))
        sqlite_connection.commit()

        await message.answer(dialog.NEW_ADMIN_FINAL)
        await Bot.send_message(all_for_admin[0], dialog.NEW_ADMIN_FINAL_TO)
        await state.finish()
    else:
        cursor.execute("UPDATE Stuff SET Stuff_state = 0 WHERE (Stuff_id = ?", message.from_user.id)
        sqlite_connection.commit()


@bot.message_handler(lambda message: message.text == 'Добавить Kонcультанта')
async def Add_Konsultant(message: types.Message):

    cursor.execute("SELECT Stuff_status FROM Stuff WHERE Stuff_id = ?", message.from_user.id)
    proverka_na_prava_konsultant = str(cursor.fetchone())

    if proverka_na_prava_konsultant == '(6,)'\
            or proverka_na_prava_konsultant == '(5,)'\
            or proverka_na_prava_konsultant == '(4,)':

        await states.S_ENTER_ID_Konsultant.set()
        await message.answer(dialog.NEW_KONSULTANT, reply_markup=K.reply_keyboard('back_action'))
    else:
        await message.answer(f"Недостаточно прав {proverka_na_prava_konsultant}")


@bot.message_handler(state=states.S_ENTER_ID_Konsultant)
async def S_ENTER_ID_Admin(message: Message, state: FSMContext):
    if message.text != 'Назад':
        all_for_admin = str(message.text).split('-')
        print(message.text, all_for_admin)
        cursor.execute("INSERT INTO Stuff VALUES (?, ?, ?, ?, ?)",
                       (all_for_admin[0], all_for_admin[1].lstrip(), 3, 0, 0))
        sqlite_connection.commit()

        await message.answer(dialog.NEW_KONSULTANT_FINAL)
        await Bot.send_message(all_for_admin[0], dialog.NEW_KONSULTANT_FINAL_TO)
        await state.finish()
    else:
        cursor.execute("UPDATE Stuff SET Stuff_state = 0 WHERE (Stuff_id = ?", message.from_user.id)
        sqlite_connection.commit()
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------#


# Необработанные сообщения
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------#
@bot.message_handler()
async def handle_text(message: Message):
    await message.answer(dialog.TEXT_RANDOM)
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------#


# Запускаем бота
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------#
if __name__ == '__main__':
    executor.start_polling(bot)
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------#
