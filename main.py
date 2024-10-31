from PIL import Image
import pytesseract
import logging


class TextExtractor:
    def __init__(self, image_path: str):
        self.image_path = image_path
        self.processed_image = None
        self.image = None

        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    def its(self):
        return pytesseract.image_to_string(Image.open(self.path + self.file), self.lang)


if __name__ == '__main__':
    do = TextExtractor('1.jpg')
    print(do.its())
    
