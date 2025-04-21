import time
import pytest
from pages.base_class import BaseClass
from playwright.sync_api import sync_playwright, Page, Dialog, BrowserContext

class TestAlert:


    """Тест по Алертам"""
    @pytest.mark.alert
    def test_alert(self, page:Page):
        page.goto("https://demoblaze.com")

        #Функция по обработке алерта
        def accept_alert(alert:Dialog):
            print(alert.message)
            alert.accept()

        page.on("dialog", accept_alert)
        page.get_by_role("link", name="Samsung galaxy s6").click()
        page.get_by_role("link", name="Add to cart").click()
        page.wait_for_event("dialog")
        page.locator("#cartur").click()
        time.sleep(5)


    """Тест по вкладкам"""
    @pytest.mark.tabs
    def test_tabs(self, page:Page, context:BrowserContext):
        page.goto("https://nomads.com/")
        with context.expect_page() as new_tab_event:
            page.get_by_alt_text("Get insured").click()
        new_tab = new_tab_event.value
        new_tab.locator("[data-testid='ni-landing-sign-me-up-button']").click()


    """Тест по iframe"""
    @pytest.mark.iframe
    def test_iframe(self, page:Page):
        page.goto("https://www.qa-practice.com/elements/iframe/iframe_page")
        page.frame_locator("iframe").locator(".navbar-toggler-icon").click()
        time.sleep(5)


    """Тест по селекту"""
    @pytest.mark.select
    def test_select(self, page):
        page.goto("https://magento.softwaretestingboard.com/men/tops-men/jackets-men.html")
        page.locator("#sorter").first.select_option("Product Name")
        time.sleep(5)
