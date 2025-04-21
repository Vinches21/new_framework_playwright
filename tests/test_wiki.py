import time

import pytest
from playwright.sync_api import Page, expect, Route
import  re




@pytest.mark.wiki
def test_wiki(page:Page):
    page.goto("https://www.wikipedia.org/")
    page.get_by_role("link", name="Русский").click()
    expect(page.get_by_text("Добро пожаловать в Википедию,")).to_be_visible()
    time.sleep(5)

@pytest.mark.wiki2
def test_wiki2(page:Page):
    page.goto("https://www.wikipedia.org/")
    page.get_by_role("link", name="Русский").click()
    page.get_by_role("link", name="Содержание").click()
    page.locator("#ca-talk").click()
    expect(page.locator("#firstHeading")).to_have_text("Обсуждение Википедии:Содержание")


"""Тест по подмене запроса с фронта"""
@pytest.mark.req
def test_request(page:Page):
    def change_request(route: Route):
        data = route.request.post_data
        if data:
            data = data.replace("User412", "User413lhlkhlhlh")
        route.continue_(post_data=data)
    page.route(re.compile("profile/authenticate/"), change_request)
    page.goto("https://gymlog.ru/profile/login/")
    page.locator("#email").fill("User412")
    page.locator("#password").fill("qwerty")
    page.get_by_role("button", name="Войти").click()
    time.sleep(5)


"""Тест по подмене бэкового ответа"""
@pytest.mark.res
def test_response(page:Page):
    def change_response(route:Route):
        response = route.fetch()
        data = response.text()
        data = data.replace("User4815", "Nobody")
        route.fulfill(response=response, body=data)
    page.route(re.compile("profile/"), change_response)
    page.goto("https://gymlog.ru/profile/login/")
    page.locator("#email").fill("User4815")
    page.locator("#password").fill("qwerty")
    page.get_by_role("button", name="Войти").click()
    page.get_by_role("link", name="Мой профиль").click()