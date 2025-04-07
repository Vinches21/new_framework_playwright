import functools
import time
import pytest
from pages.base_class import BasePage


def trace_step(name):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            page = kwargs.get('page') or next((arg for arg in args if hasattr(arg, 'context')), None)
            if page:
                page.context.tracing.start_chunk(name=name)
                try:
                    return func(*args, **kwargs)
                finally:
                    page.context.tracing.stop_chunk()
            return func(*args, **kwargs)
        return wrapper
    return decorator

class TestLesson:

    @pytest.mark.one
    def test_open_page_positive(self, page):
        """Проверка открытия страницы"""
        base_page = BasePage(page)
        base_page.open_url("https://ya.ru")
        assert 'Яндекс — быстрый поиск в интернете' in page.title()
        time.sleep(2)

    @pytest.mark.one
    def test_open_page_negаtive(self, page):
        """Проверка открытия страницы"""
        base_page = BasePage(page)
        base_page.open_url("https://ya.ru")
        assert 'Яндекс — быстрый поис в интернете' in page.title()
        time.sleep(2)

    def test_search_on_google(self, page):
        """Тест поиска в Google"""
        base_page = BasePage(page)
        base_page.open_url("https://google.com")

        #Принимаем куки (если есть попал)
        if base_page.is_visible('button:has-text("Accept all")'):
            base_page.click('button:has-text("Accept all")')

        base_page.fill('//textarea[@id="APjFqb"]', "Playwright Python")
        base_page.click("(//span[text() = 'playwright python'])[1]")
        base_page.wait_for_selector('text="Playwright"')
        assert "Playwright" in base_page.get_text('h3')