import logging
import os
from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.utils.executor import start_webhook
from aiogram import Bot, types
from db import *
from messages import *
import asyncio


TOKEN = os.getenv('BOT_TOKEN')
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
main_dp = Dispatcher(bot)

HEROKU_APP_NAME = os.getenv('HEROKU_APP_NAME')

# webhook settings
WEBHOOK_HOST = f'https://{HEROKU_APP_NAME}.herokuapp.com'
WEBHOOK_PATH = f'/webhook/{TOKEN}'
WEBHOOK_URL = f'{WEBHOOK_HOST}{WEBHOOK_PATH}'

# webserver settings
WEBAPP_HOST = '0.0.0.0'
WEBAPP_PORT = os.getenv('PORT', default=8000)


logging.basicConfig(level=logging.INFO)

async def on_startup(dispatcher):
	await bot.set_webhook(WEBHOOK_URL, drop_pending_updates=True)


async def on_shutdown(dispatcher):
	await bot.delete_webhook()


@dp.message_handler(commands=['start'])
async def process_start_cmd(message: types.Message):
	keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True).add(START_KB_TEXT_1, START_KB_TEXT_2)
	await message.answer(START_CMD_MESSAGE_1, reply_markup=keyboard)
	await db_add_user(message.from_user.id)

@dp.message_handler(commands=['help'])
async def process_help_cmd(message: types.Message):
	await message.answer(HELP_CMD_MESSAGE_1)

@dp.message_handler(lambda message: message.text == START_KB_TEXT_1)
async def process_my_chats_cmd(message: types.Message):
	await message.answer("penis")

async def start_main_bot():
	await start_webhook(
		dispatcher=main_dp,
		webhook_path=WEBHOOK_PATH,
		skip_updates=True,
		on_startup=on_startup,
		on_shutdown=on_shutdown,
		host=WEBAPP_HOST,
		port=WEBAPP_PORT,
	)
	
async def start_sub_bots():
	await start_webhook(
		dispatcher=dp,
		webhook_path=WEBHOOK_PATH,
		skip_updates=True,
		on_startup=on_startup,
		on_shutdown=on_shutdown,
		host=WEBAPP_HOST,
		port=WEBAPP_PORT,
	)
	
async def start_bots():
	await asyncio.gather([asyncio.create_task(start_main_bot()), asyncio.create_task(start_sub_bots())])
	
if __name__ == '__main__':
	#asyncio.run(start_bots())
	start_webhook(
		dispatcher=dp,
		webhook_path=WEBHOOK_PATH,
		skip_updates=True,
		on_startup=on_startup,
		on_shutdown=on_shutdown,
		host=WEBAPP_HOST,
		port=WEBAPP_PORT,
	)
