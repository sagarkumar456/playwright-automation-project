class PaymentPage:

    def __init__(self, page):
        self.page = page
        self.razorpay_iframe = "iframe[src*='razorpay']"

    def razorpay_Contact_details(self, mobile_number):
        # Wait for iframe
        self.page.wait_for_selector(self.razorpay_iframe, timeout=60000)

        # Switch to Razorpay iframe
        frame = self.page.frame(url=lambda url: url and "razorpay" in url)

        # Enter mobile number
        frame.get_by_test_id("contactNumber").fill(mobile_number)

        # Click Skip OTP
        frame.get_by_text("Skip OTP", exact=True).click()

        # Optional: wait for success
        self.page.wait_for_timeout(5000)