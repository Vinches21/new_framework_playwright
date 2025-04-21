
import random
import time
from random import randint
from typing import Optional

from playwright.sync_api import Page, FrameLocator

class BaseClass:
    def __init__(self, page: Page):
        self.page = page
        self.current_frame = None  # Только None или FrameLocator

    @property
    def current_frame(self) -> Optional[FrameLocator]:
        """Геттер с защитой от некорректных значений."""
        if self._current_frame is not None and not isinstance(self._current_frame, FrameLocator):
            raise TypeError(
                f"current_frame должен быть FrameLocator или None, получен {type(self._current_frame)}. "
                f"Значение: {self._current_frame}"
            )
        return self._current_frame

    @current_frame.setter
    def current_frame(self, value):
        """Сеттер с валидацией типа."""
        if value is not None and not isinstance(value, FrameLocator):
            actual_type = type(value)
            # Если это кортеж, выведем его содержимое для отладки
            if isinstance(value, tuple):
                raise TypeError(
                    f"Недопустимое присвоение кортежа в current_frame: {value}. "
                    f"Возможно, какой-то метод возвращает несколько значений?"
                )
            raise TypeError(
                f"current_frame принимает только FrameLocator или None, получен {actual_type}"
            )
        self._current_frame = value

    def switch_to_frame(self, locator: str) -> 'BaseClass':
        """Переключение на фрейм с гарантией сохранения типа."""
        frame_locator = self.page.frame_locator(locator)
        self.current_frame = frame_locator  # Используем сеттер
        return self  # Для поддержки цепочки вызовов

    """Открыть URL."""
    def open_url(self, url: str):
        self.page.goto(url)

    # """Переключение на фрейм и сохранение контекста"""
    # def switch_to_frame(self, locator):
    #     self.current_frame = self.page.frame_locator(locator)
    #     return self.current_frame

    """Возврат к основному контенту"""
    def switch_to_default(self):
        self.current_frame = None

    def wait_and_get_element(self, selector: str):
        """Полностью безопасный вариант."""
        if self.current_frame is not None:
            return self.current_frame.locator(selector).first
        return self.page.locator(selector).first

    def element_is_present(self, selector: str, timeout=50_000):
        """Безопасный поиск элементов."""
        try:
            if self.current_frame:
                locator = self.current_frame.locator(selector)
            else:
                locator = self.page.locator(selector)

            # Явная проверка типа
            if not hasattr(locator, 'all'):
                raise TypeError(f"Некорректный locator: {type(locator)}")

            locator.first.wait_for(state="attached", timeout=timeout)
            return locator

        except Exception as e:
            print(f"Ошибка в element_all_present: {e}")
            return []


    def element_all_present(self, selector: str, timeout=50_000):
        """Безопасный поиск элементов."""
        try:
            if self.current_frame:
                locator = self.current_frame.locator(selector)
            else:
                locator = self.page.locator(selector)

            # Явная проверка типа
            if not hasattr(locator, 'all'):
                raise TypeError(f"Некорректный locator: {type(locator)}")

            locator.first.wait_for(state="attached", timeout=timeout)
            return locator.all()

        except Exception as e:
            print(f"Ошибка в element_all_present: {e}")
            return []

    # """Получение всех элементов"""
    # def element_all_present(self, selector: str, timeout=10_000):
    #     locator = self.current_frame.locator(selector) if self.current_frame else self.page.locator(selector)
    #     locator.first.wait_for(state="attached", timeout=timeout)
    #     return locator.all()

    """Кликнуть на элемент"""
    def click_to_element(self, selector: str):
        element = self.wait_and_get_element(selector)
        element.click(timeout=60000)

    def click_hover(self, parent: str, child: str):
        parent = self.wait_and_get_element(parent)
        if parent.count() == 0:
            raise Exception("Родительский элемент не найден")
        parent.hover()
        # Ждем появления элемента и кликаем
        # element = self.wait_and_get_element(child).wait_for(state='visible')
        element = self.wait_and_get_element(child)
        element.click()

    """Заполнить поле ввода текстом"""
    def fill_text(self, selector: str, text: str):
        """Защищённый метод заполнения текста."""
        try:
            element = self.wait_and_get_element(selector)
            element.wait_for(state="attached")
            element.fill(text)
        except Exception as e:
            current_frame_type = type(self._current_frame).__name__
            raise RuntimeError(
                f"Ошибка в fill_text. Текущий фрейм: {current_frame_type}, "
                f"селектор: '{selector}'. Ошибка: {str(e)}"
            ) from e

    """Последовательное нажатие клавиш"""
    def fill_text_with_keys(self, selector: str, text: str):
        """Защищённый метод заполнения текста."""
        try:
            element = self.wait_and_get_element(selector)
            element.wait_for(state="attached")
            element.type(text)
        except Exception as e:
            current_frame_type = type(self._current_frame).__name__
            raise RuntimeError(
                f"Ошибка в fill_text. Текущий фрейм: {current_frame_type}, "
                f"селектор: '{selector}'. Ошибка: {str(e)}"
            ) from e


    """Нахождение по тексту"""
    def find_by_text(self, text: str):
        if self.current_frame is not None:
            return self.current_frame.get_by_text(text)
        return self.page.get_by_text(text)


    """Очистка поля ввода"""
    def clear_text(self, selector: str):
        """Защищённый метод очистки текста."""
        try:
            element = self.wait_and_get_element(selector)
            element.wait_for(state="attached")
            element.fill("")
        except Exception as e:
            current_frame_type = type(self._current_frame).__name__
            raise RuntimeError(
                f"Ошибка в fill_text. Текущий фрейм: {current_frame_type}, "
                f"селектор: '{selector}'. Ошибка: {str(e)}"
            ) from e

    """Ввод текста в поле ввода с помощью JavaScript"""

    def wait_for_selector(self, selector: str, timeout: int = 5000):
        """Ожидать появления элемента."""
        self.page.wait_for_selector(selector, timeout=timeout)

    def is_visible(self, selector: str) -> bool:
        """Проверить, видим ли элемент."""
        return self.page.is_visible(selector)



    def click_on_react_select(self, data_test_id, id_categories=None):
        self.click_to_element(f"[data-testid={data_test_id}] .bcp-select__control")
        if id_categories is None:
            items = self.element_all_present(f"[data-testid={data_test_id}] .bcp-select__option")
            random_el = randint(1, len(items))
            self.click_to_element(f"[data-testid={data_test_id}] .bcp-select__option:nth-child({random_el})")
        else:
            self.click_to_element(f"[data-testid={data_test_id}] .bcp-select__option:nth-child({id_categories})")


    """Выбор рандомного актива в файлпикере"""
    def click_to_asset(self, data_test_id="asset-chooser-loader", element=None):
        if element is None:
            items = self.element_all_present(f"[data-testid={data_test_id}] .AssetPreview_card__fPONE")
            random_el = random.randint(1, len(items))
            elem = f"[data-testid={data_test_id}] .AssetPreview_card__fPONE:nth-child({random_el}) > div:nth-of-type(1)"
        else:
            elem = f"[data-testid={data_test_id}] .AssetPreview_card__fPONE:nth-child(1) > div:nth-of-type(1)"
        self.click_to_element(elem)


    """Ввод текста в селект и выбор значения"""
    def input_on_react_select(self, data_test_id, text):
        self.fill_text(f"[data-testid={data_test_id}] .bcp-select__control input", text)
        time.sleep(1)
        items = self.element_all_present(f"[data-testid={data_test_id}] .bcp-select__option")
        random_el = random.randint(1, len(items))
        self.click_to_element(f"[data-testid={data_test_id}] .bcp-select__option:nth-child({random_el})")


    """Метод по сохранению компонента в сайдбаре"""
    def save_component_in_sidebar(self):
        # self.element_is_clickable((By.XPATH, "(//span[text()='Сохранить'])[2]")).click()
        # self.click_to_element(self.element_is_present((By.XPATH, '(//button[.//span[text()="Сохранить"]])[2]')))
        self.click_to_element(fr"(//span[text()='Сохранить'])[2]")


    """Метод получения url"""
    def get_current_url(self):
        return self.page.url


    """Метод по имитации клавищ"""
    def press_keys(self, key: str):
        self.page.keyboard.press(key)


    """Метод по получению текста из элемента"""
    def get_text_from_element(self, selector: str):
        element = self.wait_and_get_element(selector)
        # return element.inner_text()
        return element.text_content()


    """Метод по получению значения из атрибута элемента"""
    def get_value_from_attr(self, selector: str, attr):
        element = self.wait_and_get_element(selector)
        # return element.inner_text()
        return element.get_attribute(attr)


    """Метод по проверке статус кода запроса"""
    def get_response(self, point, selector):
        # Кликаем на кнопку и ждем ответа
        with self.page.expect_response(point) as response_info:
            self.click_to_element(selector)
        response = response_info.value
        print(response.json())
        return response