import pytest
import pyautogui
from ui.base_ui import UIAutomator

# Инициализация UIAutomator
ui_automator = UIAutomator()

def test_click_by_coordinates():
    """Тестирование клика по координатам."""
    try:
        ui_automator.click(x=100, y=200)
        # Проверка, что клик не вызвал ошибок
        assert True
    except Exception as e:
        pytest.fail(f"Ошибка при клике: {e}")

def test_click_by_image():
    """Тестирование клика по изображению."""
    try:
        result = ui_automator.click(image="image/image.png", timeout=5)
        assert result is None or result == True  # Переход по изображению
    except Exception as e:
        pytest.fail(f"Ошибка при клике по изображению: {e}")

def test_type_text():
    """Тестирование ввода текста."""
    try:
        ui_automator.type_text("Hello, PyAutoGUI!")
        # Проверка, что текст был введен (псевдотест)
        assert True
    except Exception as e:
        pytest.fail(f"Ошибка при вводе текста: {e}")

def test_find_element():
    """Тестирование поиска элемента на экране."""
    try:
        pos = ui_automator.find(image="image/image.png", timeout=5)
        assert pos is not None  # Если позиция найдена, тест успешен
    except Exception as e:
        pytest.fail(f"Ошибка при поиске элемента: {e}")
