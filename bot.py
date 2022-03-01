import logging

from aiogram import Bot, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.dispatcher.webhook import SendMessage
from aiogram.dispatcher import Dispatcher
from aiogram.utils.executor import start_webhook

# aiogram ↑ Foreign ↓

from textblob import TextBlob
import sqlite3


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

logging.basicConfig(level = logging.INFO)

bot = Bot(token = API_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())

#Inline Keyboard ↓

btn1 = InlineKeyboardButton('🇺🇸 Англиский 🇬🇧', callback_data = 'button1')
btn2 = InlineKeyboardButton('🇪🇸 Испанский 🇪🇸', callback_data = 'button2')
btn3 = InlineKeyboardButton('🇫🇷 Французский 🇫🇷', callback_data = 'button3')
btn4 = InlineKeyboardButton('🇩🇪 Немецкий 🇩🇪', callback_data = 'button4')
btn5 = InlineKeyboardButton('🇨🇳 Китайский 🇨🇳', callback_data = 'button5')
btn6 = InlineKeyboardButton('🇯🇵 Японский 🇯🇵', callback_data = 'button6')
btn7 = InlineKeyboardButton('🇷🇺 Русский 🇷🇺', callback_data = 'button7')
Ikb1 = InlineKeyboardMarkup(row_width = 2).add(btn1, btn2, btn3, btn4, btn5, btn6, btn7)



@dp.message_handler(commands = ['start'])
async def hi(msg: types.Message):
    conn = sqlite3.connect('gTranslate.db', check_same_thread = False)

    cursor = conn.cursor()
    cursor.execute(f"SELECT UTEXT FROM PHRASE WHERE ID = {msg.chat.id}")
    data = cursor.fetchone()

    if data is None:
        cursor.execute("""
        INSERT INTO PHRASE (ID, UTEXT) 
        VALUES (?, ?)
        """,(msg.chat.id,'Some text'))
        conn.commit()
      
    else:
        pass
    conn.close()

    return SendMessage(msg.chat.id, "Пришли текст, я переведу!")

@dp.message_handler()
async def translate(msg: types.Message):
    conn = sqlite3.connect('gTranslate.db', check_same_thread = False)
    conn.execute("UPDATE PHRASE SET UTEXT=? WHERE ID=?",(msg.text.replace(';','').replace("union",''), msg.chat.id))
    conn.commit()
    conn.close()
    return SendMessage(msg.chat.id, f"На какой язык хотите перевести?\n\n*→ {msg.text.replace(';','').replace('union','')} ←*", reply_markup = Ikb1, parse_mode="Markdown")


### Ответы на кнопки ↓

# English

@dp.callback_query_handler(text = 'button1')
async def translate_to_en(callback_query: types.CallbackQuery):
    conn = sqlite3.connect('gTranslate.db', check_same_thread = False)
    cursor = conn.cursor()
    cursor.execute(f"SELECT UTEXT FROM PHRASE WHERE ID={callback_query.from_user.id}")
    data = cursor.fetchone()
    conn.close()
    await bot.answer_callback_query(callback_query.id)
    try:
        return SendMessage(callback_query.from_user.id, text=TextBlob(str(data).replace('(','').replace(')','').replace("'",'').replace(",",'')).translate(to = 'en'))
    except:
        return SendMessage(callback_query.from_user.id, "Ошибка :c")

# Spanish

@dp.callback_query_handler(text = 'button2')
async def translate_to_sp(callback_query: types.CallbackQuery):
    conn = sqlite3.connect('gTranslate.db', check_same_thread = False)
    cursor = conn.cursor()
    cursor.execute(f"SELECT UTEXT FROM PHRASE WHERE ID={callback_query.from_user.id}")
    data = cursor.fetchone()
    conn.close()
    await bot.answer_callback_query(callback_query.id)
    try:
        return SendMessage(callback_query.from_user.id, TextBlob(str(data).replace('(','').replace(')','').replace("'",'').replace(",",'')).translate(to = 'es'))
    except:
        return SendMessage(callback_query.from_user.id, "Ошибка :c")

# French

@dp.callback_query_handler(text = 'button3')
async def translate_to_ch(callback_query: types.CallbackQuery):
    conn = sqlite3.connect('gTranslate.db', check_same_thread = False)
    cursor = conn.cursor()
    cursor.execute(f"SELECT UTEXT FROM PHRASE WHERE ID={callback_query.from_user.id}")
    data = cursor.fetchone()
    conn.close()
    await bot.answer_callback_query(callback_query.id)
    try:
        return SendMessage(callback_query.from_user.id, TextBlob(str(data).replace('(','').replace(')','').replace("'",'').replace(",",'')).translate(to = 'fr'))
    except:
        return SendMessage(callback_query.from_user.id, "Ошибка :c")

# German

@dp.callback_query_handler(text = 'button4')
async def translate_to_ger(callback_query: types.CallbackQuery):
    conn = sqlite3.connect('gTranslate.db', check_same_thread = False)
    cursor = conn.cursor()
    cursor.execute(f"SELECT UTEXT FROM PHRASE WHERE ID={callback_query.from_user.id}")
    data = cursor.fetchone()
    conn.close()
    await bot.answer_callback_query(callback_query.id)
    try:
        return SendMessage(callback_query.from_user.id, TextBlob(str(data).replace('(','').replace(')','').replace("'",'').replace(",",'')).translate(to = 'de'))
    except:
        return SendMessage(callback_query.from_user.id, "Ошибка :c")

# Chinese

@dp.callback_query_handler(text = 'button5')
async def translate_to_ger(callback_query: types.CallbackQuery):
    conn = sqlite3.connect('gTranslate.db', check_same_thread = False)
    cursor = conn.cursor()
    cursor.execute(f"SELECT UTEXT FROM PHRASE WHERE ID={callback_query.from_user.id}")
    data = cursor.fetchone()
    conn.close()
    await bot.answer_callback_query(callback_query.id)
    try:
        return SendMessage(callback_query.from_user.id, TextBlob(str(data).replace('(','').replace(')','').replace("'",'').replace(",",'')).translate(to = 'zh'))
    except:
        return SendMessage(callback_query.from_user.id, "Ошибка :c")

# Japanese

@dp.callback_query_handler(text = 'button6')
async def translate_to_ger(callback_query: types.CallbackQuery):
    conn = sqlite3.connect('gTranslate.db', check_same_thread = False)
    cursor = conn.cursor()
    cursor.execute(f"SELECT UTEXT FROM PHRASE WHERE ID={callback_query.from_user.id}")
    data = cursor.fetchone()
    conn.close()
    await bot.answer_callback_query(callback_query.id)
    try:
        return SendMessage(callback_query.from_user.id, TextBlob(str(data).replace('(','').replace(')','').replace("'",'').replace(",",'')).translate(to = 'ja'))
    except:
        return SendMessage(callback_query.from_user.id, "Ошибка :c")


@dp.callback_query_handler(text = 'button7')
async def translate_to_ger(callback_query: types.CallbackQuery):
    conn = sqlite3.connect('gTranslate.db', check_same_thread = False)
    cursor = conn.cursor()
    cursor.execute(f"SELECT UTEXT FROM PHRASE WHERE ID={callback_query.from_user.id}")
    data = cursor.fetchone()
    conn.close()
    await bot.answer_callback_query(callback_query.id)
    try:
        return SendMessage(callback_query.from_user.id, TextBlob(str(data).replace('(','').replace(')','').replace("'",'').replace(",",'')).translate(to = 'ru'))
    except:
        return SendMessage(callback_query.from_user.id, "Ошибка :c")

# On_startup / On_shutdown

async def on_startup(dp):
    await bot.set_webhook(WEBHOOK_URL)
    # insert code here to run it after start


async def on_shutdown(dp):
    logging.warning('Shutting down..')

    # insert code here to run it before shutdown

    await bot.delete_webhook()

    conn.close()
    await dp.storage.close()
    await dp.storage.wait_closed()

    logging.warning('Bye!')



if __name__=='__main__':
    start_webhook(
        dispatcher=dp,
        webhook_path=WEBHOOK_PATH,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        skip_updates=True,
        host=WEBAPP_HOST,
        port=WEBAPP_PORT,
    )
