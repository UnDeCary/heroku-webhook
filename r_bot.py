from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

import logging

from aiogram import Bot, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.dispatcher.webhook import SendMessage, SendInvoice, EditMessageText, AnswerPreCheckoutQuery
from aiogram.dispatcher import Dispatcher
from aiogram.utils.executor import start_webhook

# aiogram ↑ Foreign ↓

import asyncio
import sqlite3

PROVIDER_TOKEN = '410694247:TEST:e81b43d7-32c6-4a59-8297-1747a94689fa'

# Variables ↓

API_TOKEN = '1646981030:AAGYMP-_SjuqJqhJguI9GccCAv2Wso6hQnE'

# webhook settings

WEBHOOK_HOST = 'https://masterbookapp.com'
WEBHOOK_PATH = '/bot/'
WEBHOOK_URL = f'{WEBHOOK_HOST}{WEBHOOK_PATH}'

# webserver settings

WEBAPP_HOST = 'localhost'
WEBAPP_PORT = 7007

# bot settings + logging ↓

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    conn = sqlite3.connect('Raffle.db', check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM Members WHERE CHAT_ID={message.from_user.id}")
    data = cursor.fetchall()
    cursor.execute(f"SELECT * FROM Members")
    max = cursor.fetchall()

    if data == []:
        return SendMessage(message.from_user.id, '''Привет!\n\nЭтот бот сделан для организации розыгрыша среди учеников *гимназии №60*
Период регистрации *25 апреля* - *25 мая*
Макс. число участников - *250 человек*
Оглошение результатов 25 мая на линейке.\nРозыгрываются 2 самоката:\n*МОДЕЛЬ 1*\n*МОДЕЛЬ 2*\n
Участие стоит *1.000 ₸*.\nЧтобы присединиться, оплатите счет ↓ ''',
                               reply_markup = InlineKeyboardMarkup().add(InlineKeyboardButton('Записаться', callback_data='Order')),
                               parse_mode='MARKDOWN')
    elif len(max) == 250:
        return SendMessage(message.from_user.id, 'Набор участников закрыт')

    else:
        cursor.execute(f"SELECT Number FROM Members WHERE CHAT_ID={message.from_user.id}")
        return SendMessage(message.from_user.id, f'Вы уже принимаете участие, ваш номер *{cursor.fetchone()[0]}*', parse_mode='MARKDOWN')
    conn.close()

@dp.message_handler(commands=['show'])
async def show(message: types.Message):
    if message.from_user.id == 825292339:
        msg = message.text.split()
        conn = sqlite3.connect('Raffle.db', check_same_thread=False)
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM Members WHERE Number={int(msg[1])}")
        return SendMessage(message.from_user.id, cursor.fetchall())
    else:
        pass
    
    
    
    
@dp.callback_query_handler(text='Order')
async def order(call: types.CallbackQuery):
    conn = sqlite3.connect('Raffle.db', check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM Members")
    max = cursor.fetchall()

    if len(max) == 250:
        return SendMessage(call.from_user.id, 'Набор участников закрыт')
    
    else:

        await call.message.edit_text('''Привет!\n\nЭтот бот сделан для организации розыгрыша среди учеников *гимназии №60*
        Период регистрации *25 апреля* - *25 мая*
        Оглошение результатов 25 мая на линейке.\nРозыгрываются 2 самоката:\n*МОДЕЛЬ 1*\n*МОДЕЛЬ 2*\n
        Участие стоит *1.000 ₸*.\nЧтобы присединиться, оплатите счет ↓ ''',
                                     reply_markup = InlineKeyboardMarkup().add(InlineKeyboardButton(' ', callback_data='nothing')),
                                     parse_mode='MARKDOWN')
    
        return SendInvoice(call.from_user.id,
                               title='Принять участие',
                               description=f'''После оплаты вы получите номер, среди всех номеров на линейке будет выбранно 2 номера случайным образом\n
    Именно ты имеешь шанс получить один из 2-х самокатов''',
                               provider_token=PROVIDER_TOKEN,
                               currency='kzt',
                               need_name=True,
                               need_phone_number=True,
                               prices=[types.LabeledPrice(label=f"Принять участие", amount=100000)],
                               start_parameter='product',
                               payload='payload-for-internal-use'
                               )

@dp.pre_checkout_query_handler(lambda query: True)
async def process_pre_checkout_query(pre_query: types.PreCheckoutQuery):
    return AnswerPreCheckoutQuery(pre_query.id, ok=True, error_message='Что-то пошло не так, повторите попытку!')

@dp.message_handler(content_types=['successful_payment'])
async def process_successful_payment(message: types.Message):
    conn = sqlite3.connect('Raffle.db', check_same_thread=False)
    cursor = conn.cursor()
    suc_p = message.successful_payment.to_python()

    conn.execute("""INSERT INTO Members (CHAT_ID, NAME, PHONE) VALUES (?, ?, ?)""", (message.from_user.id, suc_p['order_info']['name'].replace(';','').replace('union',''),
                                                                                     suc_p['order_info']['phone_number'].replace(';','').replace('union','')))
    cursor.execute(f"SELECT Number FROM Members WHERE CHAT_ID={message.from_user.id}")
    conn.commit()

    return SendMessage(message.from_user.id, f"Вы успешно зарегестрировались, Ваш номер *{cursor.fetchone()[0]}*", parse_mode='MARKDOWN')
    conn.close()


# On_startup / On_shutdown

async def on_startup(dp):
    await bot.set_webhook(WEBHOOK_URL)
    # insert code here to run it after start


async def on_shutdown(dp):
    logging.warning('Shutting down..')

    # insert code here to run it before shutdown

    await bot.delete_webhook()

    await dp.storage.close()
    await dp.storage.wait_closed()

    logging.warning('Bye!')


if __name__ == '__main__':
    start_webhook(
        dispatcher=dp,
        webhook_path=WEBHOOK_PATH,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        skip_updates=True,
        host=WEBAPP_HOST,
        port=WEBAPP_PORT,
    )
