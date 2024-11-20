import pytesseract
import logging
import cv2
import Levenshtein
import re
import sqlite3

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# логгирование отдельным классом
# обработка изображения отдельным классом
# отдельный класс для метрик
# отдельный класс для поиска в тексте (поиск ингредиентов сюда же)
# Интерфейс в виде метода save_text_to_file на основе метода process

class TextExtractor:
    def __init__(self, image_path: str):
        self.image_path = image_path
        self.processed_image = None
        self.image = None

        # Настройка логгера с поддержкой utf-8
        logger = logging.getLogger()
        logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
        handler.setLevel(logging.INFO)
        handler.setStream(open('log.txt', 'w', encoding='utf-8'))
        logger.addHandler(handler)

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
        return extracted_text.lower()

    def extract_composition(self, text: str) -> str:
        """Извлечение состава из полного текста."""
        logging.info("Извлечение состава из текста.")

        # Регулярное выражение
        match = re.search(r'(состав:|ingredients:)(.*?\.)', text, re.IGNORECASE | re.DOTALL)

        if match:
            composition = match.group(2).strip()
            return composition.replace('\n', ' ')
        return "Состав не найден."

    def save_text_to_file(self, text: str, output_file: str):
        """Сохранение извлеченного текста в файл."""
        logging.info(f"Сохранение текста в файл {output_file}")
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(text)
        except Exception as e:
            logging.error(f"Ошибка при сохранении текста в файл: {e}")
            raise

    def calculate_wrr(self, ground_truth: str, ocr_output: str) -> float:
        """Вычисление Word Recognition Rate (WRR)."""
        logging.info("Вычисление Word Recognition Rate (WRR).")

        ground_truth_words = ground_truth.split()
        ocr_output_words = ocr_output.split()

        total_words = len(ground_truth_words)

        correctly_recognized_words = sum(1 for word in ocr_output_words if word in ground_truth_words)

        wrr = (correctly_recognized_words / total_words) * 100 if total_words > 0 else 0
        return wrr

    def calculate_cer(self, ground_truth: str, ocr_output: str) -> float:
        """Вычисление Character Error Rate (CER)."""
        logging.info("Вычисление Character Error Rate (CER).")
        distance = Levenshtein.distance(ground_truth, ocr_output)
        n = len(ground_truth)
        cer = distance / n if n > 0 else 0
        return cer

    def check_bad_ingredients(self, text: str, db_path: str, output_file: str):
        """Проверка слов в тексте на наличие в базе данных и сохранение совпадений в файл."""
        logging.info("Проверка слов на наличие в базе данных.")
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT ingredient_name FROM ingredients")
            bad_ingredients = {row[0].lower() for row in cursor.fetchall()}

            found_bad_ingredients = []
            words = re.split(r'[,\s]+', text)  # Разделение по запятым и пробелам
            for word in words:
                word = word.strip().lower()  # Очистка и приведение к нижнему регистру
                if word in bad_ingredients:
                    found_bad_ingredients.append(word)

            if found_bad_ingredients:
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write('\n'.join(found_bad_ingredients))
                logging.info(f"Найденные плохие ингредиенты сохранены в файл {output_file}")
            else:
                logging.info("Плохие ингредиенты не найдены.")

        except Exception as e:
            logging.error(f"Ошибка при проверке слов в базе данных: {e}")
            raise
        finally:
            conn.close()

    def process(self, output_file: str, ground_truth: str, db_path: str, output_bad_ingredients_file: str, blur: bool = False, adaptive: bool = False, psm: int = 6):
        """Общий метод для выполнения всех шагов обработки и извлечения текста."""
        try:
            self.load_image()
            self.preprocess_image(blur=blur, adaptive=adaptive)
            extracted_text = self.extract_text(psm=psm)

            # Извлекаем состав из полного текста
            composition = self.extract_composition(extracted_text)

            # Сохраняем состав в файл
            self.save_text_to_file(composition, output_file)

            # Проверка слов на наличие в базе данных
            self.check_bad_ingredients(composition, db_path, output_bad_ingredients_file)

            # Вычисление и вывод WRR и CER на основе состава
            wrr = self.calculate_wrr(ground_truth.lower(), composition)
            cer = self.calculate_cer(ground_truth.lower(), composition)

            logging.info(f"Состав:\n{composition}")
            logging.info(f"Word Recognition Rate (WRR): {wrr:.2f}%")
            logging.info(f"Character Error Rate (CER): {cer:.2%}")

        except Exception as e:
            logging.error(f"Ошибка в процессе обработки: {e}")

if __name__ == '__main__':
    image_path = '1.jpg'
    output_file = 'output_text.txt'
    output_bad_ingredients_file = 'output_bad_ingredients.txt'
    db_path = 'Pictures_for_tesseract.db'
    ground_truth = '''Текст'''
    extractor = TextExtractor(image_path)
    extractor.process(output_file, ground_truth, db_path, output_bad_ingredients_file, blur=False, adaptive=False, psm=6)
