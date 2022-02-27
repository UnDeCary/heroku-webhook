import os
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from flask import Flask, request

TOKEN = '1646981030:AAGYMP-_SjuqJqhJguI9GccCAv2Wso6hQnE'
URL_API = f'https://git.heroku.com/undecary-heroku.git/{TOKEN}'

bot = Bot(token = TOKEN)
dp = Dispatcher(bot)

server = Flask(__name__)

@dp.message_handler(commands=['start'])
async def hi(message: types.Message):
    await bot.send_message(message.from_user.id, f'Hi {message.from_user.first_name}')

@dp.message_handler()
async def echo(message: types.Message):
    await bot.send_message(message.from_user.id, message.text)


@server.route('/' + TOKEN, methods = ['POST'])
def get_message():
    json.string = request.get_data().decode('utf-8')
    update = types.Update.de_json(json.string)
    dp.process_updates([update])
    return '!', 200



@server.route('/')
def webhook():
    bot.delete_webhook()
    bot.set_webhook(url = APP_URL)
    return '!', 200




if __name__=='__main__':
    server.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
