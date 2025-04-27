import sys
import os
import logging
import pyautogui
import numpy as np
import cv2
from PIL import ImageGrab
import pytesseract

class UIHandler:
    def __init__(self):
        self.logger = logging.getLogger('UIHandler')
        self.logger.setLevel(logging.INFO)

    def open_application(self, application_path):
        try:
            if sys.platform == "win32":
                os.system(f"start {application_path}")
            elif sys.platform == "darwin":
                os.system(f"open {application_path}")
            else:
                os.system(f"xdg-open {application_path}")
            self.logger.info(f"Application opened: {application_path}")
        except Exception as e:
            self.logger.error(f"Error opening application: {e}")

    def close_application(self):
        pyautogui.hotkey('alt', 'f4')
        self.logger.info("Application closed")

    def click(self, x, y):
        pyautogui.click(x, y)
        self.logger.info(f"Clicked at ({x}, {y})")

    def write_text(self, text, x, y):
        self.click(x, y)
        pyautogui.write(text)
        self.logger.info(f"Text '{text}' written at ({x}, {y})")

    def find_element_opencv(self, template_path, threshold=0.8):
        """
        Ищет элемент на экране через OpenCV.
        :param template_path: путь к шаблону
        :param threshold: минимальная степень совпадения от 0 до 1
        :return: координаты (x, y) центра найденного элемента или None
        """
        screen = np.array(ImageGrab.grab())
        screen_gray = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
        template = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)

        if template is None:
            raise FileNotFoundError(f"Template not found: {template_path}")

        w, h = template.shape[::-1]
        res = cv2.matchTemplate(screen_gray, template, cv2.TM_CCOEFF_NORMED)
        loc = np.where(res >= threshold)

        if len(loc[0]) > 0:
            top_left = (loc[1][0], loc[0][0])
            center_x = top_left[0] + w // 2
            center_y = top_left[1] + h // 2
            self.logger.info(f"Element found via OpenCV: ({center_x}, {center_y})")
            return (center_x, center_y)
        else:
            self.logger.warning(f"Element not found via OpenCV: {template_path}")
            return None

    def take_screenshot(self, save_path):
        """Снимает скриншот всего экрана и сохраняет"""
        img = ImageGrab.grab()
        img.save(save_path)
        self.logger.info(f"Screenshot saved to {save_path}")

    def drag_and_drop(self, src, dst):
        """Перетаскивание из src (x,y) в dst (x,y)"""
        pyautogui.moveTo(src[0], src[1])
        pyautogui.dragTo(dst[0], dst[1], duration=0.5, button='left')
        self.logger.info(f"Dragged from {src} to {dst}")
