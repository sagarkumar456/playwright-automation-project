from playwright.sync_api import Page

class LoginPage:
    def __init__(self, page: Page):
        self.page = page
        # Locators (Using Flutter-friendly attributes)
        self.mobile_input = page.get_by_placeholder("10-digit mobile number")
        self.send_otp_button = page.get_by_role("button", name="Send OTP")
        self.otp_input = page.get_by_placeholder("Enter OTP")
        self.login_button = page.get_by_role("button", name="Login")
        self.resend_timer = page.get_by_text("Resend in")

    def load(self):
        self.page.goto("https://test.onelap.in/control/")

    def submit_mobile(self, phone_number: str):
        self.mobile_input.fill(phone_number)
        self.send_otp_button.click()

    def submit_otp(self, otp_code: str):
        # Wait for OTP field to appear before filling
        self.otp_input.wait_for(state="visible")
        self.otp_input.fill(otp_code)
        self.login_button.click()