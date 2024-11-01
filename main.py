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

    def preprocess_image(self, blur: bool = False, adaptive: bool = False):
        """Преобразование изображения в оттенки серого и бинаризация."""
        logging.info("Предобработка изображения: преобразование в серые тона и бинаризация.")
        gray_image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)

        if blur:
            gray_image = cv2.medianBlur(gray_image, 3)

        if adaptive:
            self.processed_image = cv2.adaptiveThreshold(gray_image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                                         cv2.THRESH_BINARY_INV, 11, 2)
        else:
            _, self.processed_image = cv2.threshold(gray_image, 150, 255, cv2.THRESH_BINARY_INV)

    def extract_text(self, psm: int = 6):
        """Извлечение текста из обработанного изображения."""
        if self.processed_image is None:
            logging.error("Изображение не обработано. Вызовите метод preprocess_image() перед extract_text().")
            raise ValueError("Изображение не обработано. Вызовите метод preprocess_image() перед extract_text().")
        
        logging.info(f"Извлечение текста с помощью Tesseract с параметром --psm {psm}.")
        custom_config = f'--psm {psm} -l eng+rus'  # Указываем язык
        extracted_text = pytesseract.image_to_string(self.processed_image, config=custom_config)
        return extracted_text
    