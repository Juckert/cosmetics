from aiogram import Bot, Dispatcher, F, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from tesseract import *

import os
import keyboards as kb


router = Router()

@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.reply('Привет!',reply_markup=kb.main)

@router.message(Command('help'))
async def get_help(message: Message):
    await message.answer('Отправь фото на котором полностью видна этикетка продукта и волшебным образом получишь состав')

@router.message(F.text == 'как дела?')
async def how_are_you(message: Message):
    await message.answer('Хорошо')

@router.message(F.photo)
async def get_photo(message: Message):
    await message.answer(f'ID фото: {message.photo[-1].file_id}')
    filename = message.photo[-1].file_id
    path = os.path.join(os.getcwd(), filename)
    await message.bot.download(file = filename, destination=path)
    image_path = f"{os.path.dirname(os.path.abspath(__file__))}/{filename}"
    output_file = f'output_composition{filename}.txt'
    ground_truth = '''Текст'''
    logger_instance = Logger(__name__)
    image_processor_instance = ImageProcessor(image_path=image_path, logger=logger_instance)
    composition_extractor_instance = CompositionExtractor(logger=logger_instance)

    extractor_instance = TextExtractor(image_processor=image_processor_instance,
                                       composition_extractor=composition_extractor_instance)

    extractor_instance.save_text_to_file(output_file=output_file,
                                         ground_truth=ground_truth,
                                         blur=False,
                                         adaptive=False)
    with open(f'{output_file}', 'r', encoding='utf-8') as condition:
        checker = condition.readlines()
        if os.path.exists(f'{os.path.dirname(os.path.abspath(__file__))}/{output_file}') and len(checker[0]) > 10:
            if os.path.exists(f'{os.path.dirname(os.path.abspath(__file__))}/output_bad_ingredients.txt'):
                with open('output_bad_ingredients.txt', 'r', encoding='utf-8') as file:
                    amount = 0
                    allergens_txt = ''
                    allergens = file.readlines()
                    print(allergens)
                    for element in allergens:
                        amount += 1
                        print(element[:-1])
                        allergens_txt += f'{amount}.'
                        allergens_txt += element
                await message.answer(f'Вот список потенциально опасных веществ в составе, основываясь на вашей фотографии: \n {allergens_txt}')
            else:
                await message.answer('Потенциально опасные ингридиенты не найдены')
        else:
            await message.answer('Состав не найден')
        os.remove(f'{os.path.dirname(os.path.abspath(__file__))}/output_bad_ingredients.txt')

@router.message(Command('user_info'))
async def get_help(message: Message):
    await message.reply(f'Привет.\nТвой ID: {message.from_user.id}\nИмя: {message.from_user.first_name}')