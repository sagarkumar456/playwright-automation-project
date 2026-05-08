from playwright.sync_api import Page


class LoginPage:
    def __init__(self, page: Page):
        self.page = page

        # Locators
        self.mobile_input = page.locator("input[type='tel']")
        self.send_otp_button = page.locator("button:has-text('Send Otp')")

    def enter_mobile(self, mobile):
        self.mobile_input.fill(mobile)

    def click_send_otp(self):
        self.send_otp_button.click()

    def login(self, mobile):
        self.enter_mobile(mobile)
        self.click_send_otp()