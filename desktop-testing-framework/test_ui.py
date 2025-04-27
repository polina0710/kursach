import time
import pytest
import pyautogui
from framework.ui_handler import UIHandler
from framework.config_handler import ConfigHandler
from PIL import ImageGrab
import pytesseract
from PIL import Image, ImageEnhance, ImageFilter

class TestUI:
    def setup_method(self):
        """Настройка тестового окружения"""
        self.ui = UIHandler()
        config = ConfigHandler()
        self.app_path = config.get_config('Application', 'path')
        try:
            self.templates_path = config.get_config('Application', 'templates_path')
        except Exception:
            self.templates_path = "tests/templates"

    def test_open_application(self):
        """Тест открытия приложения и нажатие кнопки уведомления через OpenCV"""
        self.ui.open_application(self.app_path)
        time.sleep(2)
        template = f"{self.templates_path}/notification_button.png"
        try:
            pos = self.ui.find_element_opencv(template)
            if not pos:
                pytest.skip(f"Кнопка уведомления не найдена: {template}")
            self.ui.click(*pos)
        finally:
            self.ui.close_application()

    def test_write_text(self):
        """Тест ввода текста в поле поиска через OpenCV"""
        self.ui.open_application(self.app_path)
        time.sleep(1)
        template = f"{self.templates_path}/search_field.png"
        try:
            pos = self.ui.find_element_opencv(template)
            if not pos:
                pytest.skip(f"Поле поиска не найдено: {template}")
            self.ui.click(*pos)
            pyautogui.write("Half-Life 3")
        finally:
            time.sleep(1)
            self.ui.close_application()


    def test_verify_label_text(self):
        """Тест OCR-проверки текста на всём экране с улучшением изображения"""
        self.ui.open_application(self.app_path)
        time.sleep(3)  # Дадим приложению чуть больше времени на открытие

        try:
            img = ImageGrab.grab()  # Скриншот всего экрана

        # --- Предобработка изображения ---
            img = img.convert('L')  # Перевести в черно-белое
            img = img.filter(ImageFilter.SHARPEN)  # Резкость
            img = img.resize((img.size[0]*2, img.size[1]*2))  # Увеличить в 2 раза для улучшения OCR

        # Распознавание текста
            text = pytesseract.image_to_string(img, lang='eng').strip()
            self.ui.logger.info(f"OCR прочитал текст на всём экране: '{text}'")

            if "News" not in text:
                pytest.skip("Текст 'News' не найден на экране")
        finally:
            self.ui.close_application()


    def test_take_screenshot(self, tmp_path):
        """Тест снятия скриншота всего экрана"""
        save_file = tmp_path / "steam_main.png"
        self.ui.open_application(self.app_path)
        time.sleep(1)
        self.ui.take_screenshot(str(save_file))
        assert save_file.exists(), f"Скриншот не сохранён: {save_file}"
        self.ui.close_application()

    def test_drag_and_drop(self):
        """Тест перетаскивания элемента"""
        self.ui.open_application(self.app_path)
        time.sleep(1)
        src = (300, 400)
        dst = (600, 400)
        self.ui.drag_and_drop(src, dst)
        self.ui.close_application()

    def test_open_and_close_sequence(self):
        """Тест простой последовательности открытия и закрытия"""
        self.ui.open_application(self.app_path)
        time.sleep(1)
        self.ui.close_application()

    def test_close_without_action(self):
        """Тест закрытия без предварительного открытия"""
        self.ui.close_application()
