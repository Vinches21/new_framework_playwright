import functools
import os
import shutil
import time

import pytest
from playwright.sync_api import Playwright, sync_playwright

def pytest_addoption(parser):
    parser.addoption("--headless", action="store_true", default=False, help="run browser in headless mode")
    parser.addoption("--playwright-trace", action="store_true", default=False, help="enable trace recording")


@pytest.fixture(scope="session")
def browser(request):
    with sync_playwright() as playwright:
        headless = request.config.getoption("--headless")
        trace_enabled = request.config.getoption("--playwright-trace")

        # Запуск браузера
        browser = playwright.chromium.launch(
            headless=headless,
            channel="chrome",
            args=[
                "--start-maximized",
                "--disable-gpu",  # Исправлено: добавлены двойные дефисы
                "--no-sandbox"  # Для linux систем
            ]
        )

        # Настройки контекста с возможностью трассировки
        context = browser.new_context(
            no_viewport=True,
            ignore_https_errors=True,
            java_script_enabled=True
        )

        if trace_enabled:
            context.tracing.start(screenshots=True, snapshots=True, sources=True)

        yield context

        # Сохраняем общий trace-файл в конце сессии
        trace_dir = "traces"
        os.makedirs(trace_dir, exist_ok=True)
        trace_path = os.path.join(trace_dir, "ALL_TESTS_TRACE.zip")
        context.tracing.stop(path=trace_path)
        print(f"\nОбщий trace файл сохранён: {os.path.abspath(trace_path)}")

        context.close()
        browser.close()


@pytest.fixture(scope="function")
def page(browser):
    page = browser.new_page()
    yield page
    page.close()

# def page(browser):
#     page = browser.new_page()
#     page.evaluate("window.moveTo(0, 0); window.resizeTo(screen.width, screen.height);")
#     page.evaluate("console.log('Important debug info')")
#
#     yield page
#     page.close()

# Хук для обработки результатов теста
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)  # сохраняем отчет в item



