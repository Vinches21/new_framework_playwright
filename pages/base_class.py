from playwright.sync_api import Page


class BasePage:
    def __init__(self, page:Page):
        self.page = page

    def open_url(self, url: str):
        """Открыть URL"""
        self.page.goto(url)

    def click(self, selector: str):
        """Клик по эдементу"""
        self.page.click(selector)

    def fill(self, selector: str, text: str):
        """Ввести текст в поле"""
        self.page.fill(selector, text)

    def get_text(self, selector: str) -> str:
        """Получить текст элемента"""
        return self.page.inner_text(selector)

    def wait_for_selector(self, selector: str, timeout: int = 5000):
        """Ожидать появление элемента"""
        self.page.wait_for_selector(selector, timeout=timeout)

    def is_visible(self, selector: str) -> bool:
        """Проверить виден ли элемент"""
        return self.page.is_visible(selector)


    def create_screenshot(self):
        screenshot_path = "screenshots/detmir_main_page.png"
        self.page.screenshot(path=screenshot_path, full_page=True)



