import os


def get_message():
    with open('../OutputMessage/output_composition.txt', 'r', encoding='utf-8') as condition:
        checker = condition.readlines()
        if os.path.exists(f'{os.path.dirname(os.path.abspath(__file__))}/OutputMessage/output_composition.txt') and len(checker[0]) > 10:
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
                os.remove(f'{os.path.dirname(os.path.abspath(__file__))}/output_bad_ingredients.txt')
                return 'Вот список потенциально опасных веществ в составе, основываясь на вашей фотографии: \n {allergens_txt}'
            else:
                return 'Потенциально опасные ингридиенты не найдены'
        else:
            return 'Состав не найден'