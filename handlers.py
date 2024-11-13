from aiogram import Bot, Dispatcher, F, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

router = Router()

@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer('Привет!')

@router.message(Command('help'))
async def get_help(message: Message):
    await message.answer('Отправь фото на котором полностью видна этикетка продукта и волшебным образом получишь состав')

@router.message(F.text == 'как дела?')
async def how_are_you(message: Message):
    await message.answer('Хорошо')

@router.message(F.photo)
async def get_photo(message: Message):
    await message.answer(f'ID фото: {message.photo[-1].file_id}')

@router.message(Command('user_info'))
async def get_help(message: Message):
    await message.reply(f'Привет.\nТвой ID: {message.from_user.id}\nИмя: {message.from_user.first_name}')