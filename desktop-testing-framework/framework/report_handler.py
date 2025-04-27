import logging
import pyautogui

class ReportHandler:
    def __init__(self):
        """Настройка логирования"""
        self.logger = logging.getLogger('ReportHandler')
        self.logger.setLevel(logging.INFO)
        ch = logging.StreamHandler()
        self.logger.addHandler(ch)

    def generate_report(self, message):
        """Генерация отчета"""
        self.logger.info(message)

    def capture_screenshot(self, filename="screenshot.png"):
        """Сохранение скриншота"""
        screenshot = pyautogui.screenshot()
        screenshot.save(filename)
        self.logger.info(f"Screenshot saved as {filename}")
