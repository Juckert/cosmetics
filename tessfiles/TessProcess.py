import pytesseract
import logging
import cv2
import Levenshtein
import re
import sqlite3

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


# Конфигурационный класс
class Config:
    DEFAULT_PSM = 6
    LANGUAGES = 'eng+rus'


# Класс для логирования
class Logger:
    def __init__(self, name: str, level=logging.INFO):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)
        if not self.logger.hasHandlers():  # Проверяем наличие обработчиков
            handler = logging.StreamHandler()
            handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
            self.logger.addHandler(handler)

    def info(self, message: str):
        self.logger.info(message)

    def error(self, message: str):
        self.logger.error(message)

    def warning(self, message: str):
        self.logger.warning(message)


# Класс для обработки изображений
class ImageProcessor:
    def __init__(self, image_path: str, logger: Logger):
        self.image_path = image_path
        self.processed_image = None
        self.image = None
        self.logger = logger

    def load_image(self):
        self.logger.info(f"Загрузка изображения из {self.image_path}")
        self.image = cv2.imread(self.image_path)
        if self.image is None:
            self.logger.error(f"Не удалось загрузить изображение: {self.image_path}")
            raise FileNotFoundError(f"Не удалось загрузить изображение: {self.image_path}")

    def preprocess_image(self, blur: bool = False, adaptive: bool = False):
        self.logger.info("Предобработка изображения.")
        gray_image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)

        if blur:
            gray_image = cv2.medianBlur(gray_image, 3)

        if adaptive:
            self.processed_image = cv2.adaptiveThreshold(gray_image, 255,
                                                         cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                                         cv2.THRESH_BINARY_INV, 11, 2)
        else:
            _, self.processed_image = cv2.threshold(gray_image, 150, 255,
                                                    cv2.THRESH_BINARY_INV)


# Класс для вычисления метрик
class Metrics:
    @staticmethod
    def calculate_wrr(ground_truth: str, ocr_output: str) -> float:
        """Вычисление Word Recognition Rate (WRR)."""
        ground_truth_words = ground_truth.split()
        ocr_output_words = ocr_output.split()

        total_words = len(ground_truth_words)

        correctly_recognized_words = sum(1 for word in ocr_output_words if word in ground_truth_words)

        wrr = (correctly_recognized_words / total_words) * 100 if total_words > 0 else 0
        return wrr

    @staticmethod
    def calculate_cer(ground_truth: str, ocr_output: str) -> float:
        """Вычисление Character Error Rate (CER)."""
        distance = Levenshtein.distance(ground_truth, ocr_output)
        n = len(ground_truth)
        cer = distance / n if n > 0 else 0
        return cer

    # Класс для извлечения состава из текста


class CompositionExtractor:
    def __init__(self, logger: Logger):
        self.logger = logger

    def extract_composition(self, text: str) -> str:
        """Извлечение состава из полного текста."""
        self.logger.info("Извлечение состава из текста.")

        # Регулярное выражение для поиска состава
        pattern = r'[\W_]*(состав|ingredients)[\W_:]*([\s\S]*?)(?:\.|$)'
        match = re.search(pattern, text, re.IGNORECASE)

        if match:
            composition = match.group(2).strip()

            # Заменяем переносы строк и объединяем части слов
            composition = re.sub(r'(\w+)-\s*(\w+)', r'\1\2', composition)
            composition = composition.replace('\n', ' ')

            # Проверяем длину извлеченного текста
            if len(composition) > 200:
                end_index = composition.find('.') + 1
                if end_index == 0:
                    end_index = len(composition)
                return composition[:end_index].strip()  # Возвращаем текст до точки
            else:
                return composition[:600].strip()  # Возвращаем первые 600 символов

        self.logger.warning("Состав не найден, возвращаем весь текст.")
        return text.replace('\n', ' ')  # Возвращаем весь текст

    def check_bad_ingredients(self, text: str, db_path: str, output_file: str):
        """Проверка фраз в тексте на наличие в базе данных и сохранение совпадений в файл."""
        self.logger.info("Проверка фраз на наличие в базе данных.")
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT ingredient_name FROM ingredients")
            bad_ingredients = {row[0].lower() for row in cursor.fetchall()}

            found_bad_ingredients = []
            phrases = re.split(r',\s*', text)  # Разделение по запятым
            for phrase in phrases:
                phrase = phrase.strip().lower()  # Очистка и приведение к нижнему регистру
                if phrase in bad_ingredients:
                    found_bad_ingredients.append(phrase)

            if found_bad_ingredients:
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write('\n'.join(found_bad_ingredients))
                self.logger.info(f"Найденные плохие ингредиенты сохранены в файл {output_file}")
            else:
                self.logger.info("Плохие ингредиенты не найдены.")

        except Exception as e:
            self.logger.error(f"Ошибка при проверке слов в базе данных: {e}")
            raise
        finally:
            conn.close()


# Класс для преобразования изображения в текст
class TextExtractor:
    def __init__(self, image_processor: ImageProcessor, composition_extractor: CompositionExtractor):
        self.image_processor = image_processor
        self.composition_extractor = composition_extractor
        self.logger = Logger(__name__)

    def extract_text(self) -> str:
        """Извлечение текста из обработанного изображения."""
        if self.image_processor.processed_image is None:
            self.logger.error("Изображение не обработано.")
            raise ValueError("Изображение не обработано.")

        self.logger.info(f"Извлечение текста с помощью Tesseract.")

        custom_config = f'--psm {Config.DEFAULT_PSM} -l {Config.LANGUAGES}'

        extracted_text = pytesseract.image_to_string(self.image_processor.processed_image, config=custom_config)

        return extracted_text.lower()

    def save_text_to_file(self, output_file: str, ground_truth: str, blur: bool = False, adaptive: bool = False):
        """Сохранение извлеченного текста в файл."""

        try:
            # Загружаем и обрабатываем изображение
            self.image_processor.load_image()
            self.image_processor.preprocess_image(blur=blur, adaptive=adaptive)

            extracted_text = self.extract_text()

            # Извлекаем состав из текста
            composition = self.composition_extractor.extract_composition(extracted_text)

            # Сохраняем состав в файл
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(composition)

            # Подсчет метрик    
            wrr = Metrics.calculate_wrr(ground_truth.lower(), composition)
            cer = Metrics.calculate_cer(ground_truth.lower(), composition)

            # self.logger.info(f"Состав:{composition}")
            self.logger.info(f"Word Recognition Rate (WRR): {wrr:.2f}%")
            self.logger.info(f"Character Error Rate (CER): {cer:.2%}")

            self.composition_extractor.check_bad_ingredients(composition, 'DataBase/Pictures_for_tesseract.db',
                                                             '../OutputMessage/output_bad_ingredients.txt')

        except Exception as e:
            self.logger.error(f"Ошибка в процессе обработки: {e}")


class DoWorkInterface:
    def __init__(self, file: str, path='images/input.jpg'):
        self.__image_path = path
        self.__output_file = file
        self.__ground_truth = '''Текст'''
        self.__logger_instance = Logger(__name__)
        self.__image_processor_instance = ImageProcessor(image_path=self.__image_path, logger=self.__logger_instance)
        self.__composition_extractor_instance = CompositionExtractor(logger=self.__logger_instance)

        self.__extractor_instance = TextExtractor(image_processor=self.__image_processor_instance,
                                                  composition_extractor=self.__composition_extractor_instance)

    def main_process(self):
        self.__extractor_instance.save_text_to_file(output_file=self.__output_file,
                                                    ground_truth=self.__ground_truth,
                                                    blur=False,
                                                    adaptive=False)


if __name__ == '__main__':
    print('It is not a lib!')
