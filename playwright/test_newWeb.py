import time

from playwright.sync_api import Playwright


def test_new_web(playwright: Playwright):
    browser=playwright.chromium.launch(headless=False)
    context=browser.new_context()
    page=context.new_page()
    page.goto("https://www.google.com")
    time.sleep(5)

