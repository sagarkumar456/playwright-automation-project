import time

from playwright.sync_api import Page, expect


def test_locators(page: Page):
    page.goto("https://r.onelap.in/test/")
    time.sleep(5)


    # playwright codegen https://rahulshettyacademy.com/client/#/auth/login