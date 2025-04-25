import time
import pyautogui
from configparser import ConfigParser

# Загрузка конфигурации
config = ConfigParser()
config.read("config/config.ini")

class UIAutomator:
    """
    Модуль для взаимодействия с элементами UI десктоп-приложения.
    Использует PyAutoGUI для всех базовых действий.
    """

    def __init__(self):
        """
        Инициализация класса UIAutomator.
        """
        pass

    def click(self, x: int = None, y: int = None, image: str = None, timeout: int = 10):
        """
        Кликает по координатам или по образу.
        :param x, y: координаты для клика
        :param image: путь до файла-образа для поиска и клика
        :param timeout: максимально ждать образ (секунд)
        """
        if image:
            # Поиск через PyAutoGUI + OpenCV
            start = time.time()
            pos = None
            while time.time() - start < timeout:
                pos = pyautogui.locateCenterOnScreen(image, confidence=0.8)
                if pos:
                    pyautogui.click(pos)
                    return
                time.sleep(0.5)
            raise RuntimeError(f"Образ {image} не найден за {timeout} секунд")
        else:
            if x is None or y is None:
                raise ValueError("Для клика по координатам необходимо указать x и y")
            pyautogui.click(x=x, y=y)

    def type_text(self, text: str, interval: float = 0.05):
        """
        Вводит текст, симулируя нажатие клавиш.
        :param text: строка для ввода
        :param interval: интервал между нажатиями
        """
        pyautogui.write(text, interval=interval)

    def scroll(self, clicks: int, x: int = None, y: int = None):
        """
        Прокручивает колесо мыши.
        :param clicks: количество "щелчков" (положительное — вверх, отрицательное — вниз)
        :param x, y: координаты, где выполнять прокрутку
        """
        pyautogui.scroll(clicks, x=x, y=y)

    def find(self, image: str, timeout: int = 10):
        """
        Ищет образ на экране.
        :param image: путь до файла-образа
        :param timeout: максимальное время ожидания (секунды)
        :return: координаты центра найденного образа или None
        """
        start = time.time()
        while time.time() - start < timeout:
            pos = pyautogui.locateCenterOnScreen(image, confidence=0.8)
            if pos:
                return pos
            time.sleep(0.5)
        return None

    def check_element_state(self, image: str):
        """
        Проверяет состояние элемента UI.
        Например, можно проверить, доступен ли элемент (кнопка) для клика.
        :param image: путь до файла-образа
        :return: True, если элемент доступен, False — если нет
        """
        pos = self.find(image)
        if pos:
            return True
        return False

    def get_element_text(self, image: str):
        """
        Получает текст с элемента, если он доступен.
        В случае с PyAutoGUI, прямое извлечение текста невозможно.
        Для более сложных задач можно использовать OCR библиотеки.
        :param image: путь до файла-образа
        :return: текст элемента (если найден), иначе None
        """
        # Прямое извлечение текста с помощью PyAutoGUI невозможно.
        # Для этого можно интегрировать OCR, например, с использованием pytesseract.
        return None
