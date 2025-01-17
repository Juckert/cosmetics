from fileinput import filename

from aiogram import Bot, Dispatcher, F, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from tesseract_func import tesseract, answer


import os
import keyboards as kb

router = Router()
answers = dict()

@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.reply('Привет!',reply_markup=kb.main)

@router.message(Command('help'))
async def get_help(message: Message):
    await message.answer('Отправь фото на котором полностью видна этикетка продукта и волшебным образом получишь состав')

@router.message(F.photo)
async def get_photo(message: Message):
    photo_id = message.photo[-1].file_id
    await message.answer(f'Ваше изображение принято, сейчас найдём вредные ингредиенты')

    filename = photo_id
    if filename in answers:
        await message.answer(answers[filename])
        return
    path = os.path.join(os.getcwd(), filename)

    await message.bot.download(file=filename, destination=path)

    tesseract(filename)
    output_message = answer(filename)

    await message.answer(output_message)
    answers[filename] = output_message


@router.message(Command('user_info'))
async def get_help(message: Message):
    await message.reply(f'Привет.\nТвой ID: {message.from_user.id}\nИмя: {message.from_user.first_name}')