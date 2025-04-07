# from playwright.sync_api import sync_playwright
#
# with sync_playwright() as p:
#     browser = p.chromium.launch(headless=False)  # Запуск браузера в видимом режиме
#     page = browser.new_page()
#     page.goto("https://example.com")
#     print(page.title())
#     browser.close()