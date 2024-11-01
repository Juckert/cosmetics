import pytesseract
import logging
import cv2

pytesseract.pytesseract.tesseract_cmd = r'Путь до tesseract'

class TextExtractor:
    def __init__(self, image_path: str):
        self.image_path = image_path
        self.processed_image = None
        self.image = None

        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    def load_image(self):
        """Загрузка изображения из файла."""
        logging.info(f"Загрузка изображения из {self.image_path}")
        self.image = cv2.imread(self.image_path)
        if self.image is None:
            logging.error(f"Не удалось загрузить изображение: {self.image_path}")
            raise FileNotFoundError(f"Не удалось загрузить изображение: {self.image_path}")