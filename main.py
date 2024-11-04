import pytesseract
import logging
import cv2
import Levenshtein
import re

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

    def process(self, output_file: str, ground_truth: str, blur: bool = False, adaptive: bool = False, psm: int = 6):
        """Общий метод для выполнения всех шагов обработки и извлечения текста."""
        try:
            self.load_image()
            self.preprocess_image(blur=blur, adaptive=adaptive)
            extracted_text = self.extract_text(psm=psm)
            
            # Извлекаем состав из полного текста
            composition = self.extract_composition(extracted_text)
            
            # Сохраняем состав в файл
            self.save_text_to_file(composition, output_file)
            
            # Вычисление и вывод WRR и CER на основе состава
            wrr = self.calculate_wrr(ground_truth.lower(), composition)
            cer = self.calculate_cer(ground_truth.lower(), composition)
            
            logging.info(f"Состав:\n{composition}")
            logging.info(f"Word Recognition Rate (WRR): {wrr:.2f}%")
            logging.info(f"Character Error Rate (CER): {cer:.2%}")

        except Exception as e:
            logging.error(f"Ошибка в процессе обработки: {e}")

if __name__ == '__main__':
    image_path = 'Путь до изображения'
    output_file = 'output_text.txt'
    
    ground_truth = '''Текст'''

    extractor = TextExtractor(image_path)
    extractor.process(output_file, ground_truth, blur=False, adaptive=False, psm=6)
    