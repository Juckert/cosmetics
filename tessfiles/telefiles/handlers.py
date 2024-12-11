from aiogram import F, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
import keyboards as kb
from logic import get_message

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.reply('Привет!',reply_markup=kb.main)


@router.message(Command('help'))
async def get_help(message: Message):
    await message.answer('Отправь фото на котором полностью видна этикетка продукта и волшебным образом получишь состав')


@router.message(F.photo)
async def get_photo(message: Message):
    await message.answer(f'ID фото: {message.photo[-1].file_id}')
    filename = message.photo[-1].file_id
    await message.bot.download(file=filename, destination='../images/input.jpg')
    await message.answer(get_message())


@router.message(Command('user_info'))
async def get_help(message: Message):
    await message.reply(f'Привет.\nТвой ID: {message.from_user.id}\nИмя: {message.from_user.first_name}')

