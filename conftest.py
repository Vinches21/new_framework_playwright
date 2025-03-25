import pytest
from playwright.sync_api import Playwright, sync_playwright

@pytest.fixture(scope="function")
def browser():
    with sync_playwright() as playwright:
        # Запуск браузера (можно изменить на 'firefox' или 'webkit'
        browser = playwright.chromium.launch(headless=False)
        yield browser
        browser.close()

@pytest.fixture(scope="function")
def page(browser):
    page = browser.new_page()
    yield page
    page.close()