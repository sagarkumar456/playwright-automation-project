from playwright.sync_api import Page

class CartPage:

    def __init__(self, page: Page):
        self.page = page
        self.place_order_btn = page.get_by_role("button", name="PLACE ORDER")
        self.razorpay_iframe = "iframe.razorpay-checkout-frame"


    def place_order(self):
        self.place_order_btn.click()

    def complete_payment(self, mobile_number):
        self.page.wait_for_selector(self.razorpay_iframe, timeout=60000)
        frame = self.page.frame(url=lambda url: url and "razorpay" in url)

        frame.get_by_test_id("contactNumber").fill(mobile_number)
        frame.get_by_text("Skip OTP", exact=True).click()