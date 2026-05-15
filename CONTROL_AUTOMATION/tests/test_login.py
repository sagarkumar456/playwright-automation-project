import pytest
from CONTROL_AUTOMATION.pages.login_page import LoginPage


def test_successful_login(page):
    login_page = LoginPage(page)

    # Step 1: Navigate to the site
    login_page.load()

    # Step 2: Enter mobile and click Send OTP
    login_page.submit_mobile("6299134504")

    # Step 3: Enter OTP (Replace '1234' with actual test OTP)
    # If the OTP is dynamic, you might need a manual pause here for testing:
    # page.pause()
    login_page.submit_otp("123456")

    # Step 4: Verification (Change this to a selector on your dashboard)
    # expect(page).to_have_url("https://test.onelap.in/control/dashboard")