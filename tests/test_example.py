from pages.base_class import BasePage


def test_open_page(page):
    """Проверка открытия страницы"""
    base_page = BasePage(page)
    base_page.open_url("https://example.com")
    assert 'Example Domain' in page.title()

def test_search_on_google(page):
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