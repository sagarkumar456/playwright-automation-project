from playwright.sync_api import sync_playwright
from sales_automation.pages.login_page import LoginPage


def test_login_flow():

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        login = LoginPage(page)

        login.open()
        login.enter_phone("6299134504")
        login.click_send_otp()

        login.enter_otp("1234")  # manual OTP
        login.click_login()

        page.wait_for_timeout(5000)
        browser.close()