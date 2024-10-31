# python.exe -m pip install --upgrade pip
# pip install pytesseract

from PIL import Image
import pytesseract


class DoWork:
    def __init__(self, file: str, lang='rus+eng', path='pic/'):
        self.lang = lang
        self.path = path
        self.file = file

    def its(self):
        return pytesseract.image_to_string(Image.open(self.path + self.file), self.lang)


if __name__ == '__main__':
    print('Use DoWork interface')
