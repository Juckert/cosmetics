from tessfiles.OutputMessage import MToken
from tessfiles.Tesseract import IToken

mm = MToken.FileChecker
im = IToken.FileChecker
prev_time = im.get_time()
__PROCESS_TOKEN__ = False


def get_message():
    with open(mm.get_path(), 'r', encoding='utf-8') as file:
        allergens_txt = ''
        allergens = file.readlines()
    return allergens_txt.join(allergens)


