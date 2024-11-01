import pytesseract
import logging

pytesseract.pytesseract.tesseract_cmd = r'Путь до tesseract'

class TextExtractor:
    def __init__(self, image_path: str):
        self.image_path = image_path
        self.processed_image = None
        self.image = None

        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')