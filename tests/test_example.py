import functools
import time

import allure
import pytest
from pages.base_class import BasePage
from playwright.sync_api import Playwright, sync_playwright, expect

@allure.feature("Тестовая фича")
class TestLesson:

    @pytest.mark.one
    @allure.title("Открыть страницу рамблера")
    def test_open_page_positive(self, page, take_screenshot):
        """Проверка открытия страницы"""
        base_page = BasePage(page)
        base_page.open_url("https://kinopoisk.ru")
        assert 'Яндекс — быстрый поиск в интернете' in page.title()
        time.sleep(2)

    @pytest.mark.one
    @allure.title("Открыть страницу яндекса")
    def test_open_page_negаtive(self, page, take_screenshot):
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

    @pytest.mark.screen
    def test_detmir_screenshot(self, page, snapshot):
        base_page = BasePage(page)
        base_page.open_url("https://kinopoisk.ru")
        # Закрытие попапа выбора региона
        # try:
        #     page.click("text=Выбрать позже", timeout=5000)
        # except:
        #     pass

        # Ожидание стабилизации страницы
        # page.wait_for_selector("h1:has-text('Детский мир')", timeout=10000)
        screenshot = page.screenshot(full_page=True)
        snapshot.assert_match(screenshot, "kinopoisk.png")

@pytest.mark.minimal
def test_minimal(image_snapshot):
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto("https://example.com")
        expect(page).to_have_screenshot("test.png")  # Проверьте это
        browser.close()