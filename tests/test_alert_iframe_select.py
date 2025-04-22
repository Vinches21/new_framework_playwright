import time
import pytest
from pages.base_class import BaseClass


class TestAlert:


    """Тест по Алертам"""
    @pytest.mark.alert
    def test_alert(self, page):
        base_page = BaseClass(page)
        base_page.open_url("https://demoblaze.com")
        base_page.allert_on()
        base_page.click_by_role("link", name="Samsung galaxy s6")
        base_page.click_by_role("link", name="Add to cart")
        base_page.wait_event("dialog")
        base_page.click_to_element("#cartur")
        time.sleep(5)


    """Тест по вкладкам"""
    @pytest.mark.tabs
    def test_tabs(self, page):
        base_page = BaseClass(page)
        base_page.open_url("https://nomads.com/")
        context = page.context
        with context.expect_page() as new_tab_event:
            base_page.click_to_element("[alt='Get insured']")
        new_tab = new_tab_event.value
        new_tab.locator("[data-testid='ni-landing-sign-me-up-button']").click()
        time.sleep(5)

    """Тест по iframe"""
    @pytest.mark.iframe
    def test_iframe(self, page):
        base_page = BaseClass(page)
        base_page.open_url("https://www.qa-practice.com/elements/iframe/iframe_page")
        base_page.switch_to_frame("iframe")
        base_page.click_to_element(".navbar-toggler-icon")
        time.sleep(5)


    """Тест по селекту"""
    @pytest.mark.select
    def test_select(self, page):
        base_page = BaseClass(page)
        base_page.open_url("https://magento.softwaretestingboard.com/men/tops-men/jackets-men.html")
        base_page.choose_value_in_select("#sorter", "Product Name")
        time.sleep(5)
