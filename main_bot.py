import asyncio
import logging
import os

from tesseract import *
from aiogram import Bot, Dispatcher, F
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from config import TOKEN
from handlers import router

bot = Bot(TOKEN)
dispatch = Dispatcher()

keyboard = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='user_info')],[KeyboardButton(text='help')]])

async def main():
    dispatch.include_router(router)
    await dispatch.start_polling(bot)

if __name__ == '__main__':
    logging.basicConfig(level = logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('EXIT')

main = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='user_info')],[KeyboardButton(text='help')]])