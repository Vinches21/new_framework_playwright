import functools
import io
import os
import shutil
import time
import pytest
from playwright.sync_api import Playwright, sync_playwright, expect
from PIL import Image
import allure

def pytest_addoption(parser):
    parser.addoption("--headless", action="store_true", default=False, help="run browser in headless mode")
    parser.addoption("--playwright-trace", action="store_true", default=False, help="enable trace recording")
    parser.addoption("--browser-t", action="store", default="chromium", choices=["chromium", "firefox", "webkit"],
                     help="Choose browser: chromium, firefox, webkit")


@pytest.fixture(scope="session")
def browser(request):
    with sync_playwright() as playwright:
        headless = request.config.getoption("--headless")
        trace_enabled = request.config.getoption("--playwright-trace")
        browser_name = request.config.getoption("--browser-t")



        # Выбираем и запускаем соответствующий браузер
        browser_type = {
            "chromium": playwright.chromium,
            "firefox": playwright.firefox,
            "webkit": playwright.webkit
        }[browser_name]

        launch_args = {
            "headless": headless,
            "args": [
                "--disable-gpu",
                "--no-sandbox",
                "--start-maximized"
            ]
        }

        # Специфичные настройки для Chromium
        if browser_name == "chromium":
            launch_args["channel"] = "chrome"

        browser = browser_type.launch(**launch_args)

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

        os.makedirs("screenshots", exist_ok=True)  # Создаем папку

        context.close()
        browser.close()


@pytest.fixture(scope="function")
def page(browser):
    page = browser.new_page()
    yield page
    page.close()

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)  # сохраняем отчет в item


def take_full_page_screenshot(page):
    # Устанавливаем размер viewport, если он не задан
    if not page.viewport_size:
        page.set_viewport_size({"width": 1280, "height": 720})

    # Получаем размеры страницы
    viewport_width = page.viewport_size["width"]
    total_height = page.evaluate("document.body.scrollHeight")
    viewport_height = page.viewport_size["height"]

    stitched_image = Image.new("RGB", (viewport_width, total_height))
    offset_y = 0

    while offset_y < total_height:
        # Скроллим страницу
        page.evaluate(f"window.scrollTo(0, {offset_y})")
        page.wait_for_timeout(500)  # Задержка для обновления страницы

        # Делаем скриншот текущей области просмотра
        screenshot = page.screenshot()
        image = Image.open(io.BytesIO(screenshot))

        # Обрезаем изображение, если оно больше высоты страницы
        if offset_y + viewport_height > total_height:
            crop_height = viewport_height - (offset_y + viewport_height - total_height)
            image = image.crop((0, viewport_height - crop_height, viewport_width, viewport_height))

        stitched_image.paste(image, (0, offset_y))
        offset_y += viewport_height

    img_byte_arr = io.BytesIO()
    stitched_image.save(img_byte_arr, format='PNG')
    return img_byte_arr.getvalue()

@pytest.fixture(scope="function")
def take_screenshot(page, request):
    yield
    if hasattr(request.node, "rep_call") and request.node.rep_call.failed:
        print("Тест упал, делаю скриншот полной страницы...")
        screenshot = take_full_page_screenshot(page)
        allure.attach(
            screenshot,
            name="Full page screenshot on failure",
            attachment_type=allure.attachment_type.PNG
        )

