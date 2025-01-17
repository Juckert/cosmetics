import os
from tesseract import *

def tesseract(filename):
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


def answer(filename):
    output_file = f'output_composition{filename}.txt'
    with open(f'{output_file}', 'r', encoding='utf-8') as condition:
        checker = condition.readlines()
        if len(checker) == 0:
            checker.append(' ')
        if os.path.exists(f'{os.path.dirname(os.path.abspath(__file__))}/{output_file}') and len(checker[0]) > 30:
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
                return f'Вот список потенциально опасных веществ в составе, основываясь на вашей фотографии: \n {allergens_txt}'
            else:
                return 'Потенциально опасные ингридиенты не найдены'
        else:
            return 'Состав не найден'