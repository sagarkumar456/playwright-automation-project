import time

from playwright.sync_api import Page


def test_HardwareKit(page: Page):
    def log_response(response):
        if "/api/" in response.url:
            print("API URL:", response.url)
            print("STATUS:", response.status)

    page.on("response", log_response)
    page.goto("https://test.onelap.in/")
    page.get_by_label("View OL vs CC GPS tracking devices comparison").click()
    page.locator("div:has-text('Hardwiring kit') span.custom-button" ).first.click()
    page.get_by_text("Add to cart", exact=True).click()
    page.get_by_text("Go to Cart", exact=True).click()
    page.locator(
        "div.summary-card:has-text('₹5790') span.material-icons:has-text('remove_circle_outline')").click()

    page.get_by_role("button", name="PLACE ORDER").click()

    # wait for Razorpay iframe
    page.wait_for_selector("iframe.razorpay-checkout-frame", timeout=60000)

    # switch to Razorpay iframe
    frame = page.frame(url=lambda url: url and "razorpay" in url)

    # enter mobile number
    frame.get_by_test_id("contactNumber").fill("6299134504")

    # SKIP OTP (correct way)
    frame.get_by_text("Skip OTP", exact=True).wait_for(timeout=30000)
    frame.get_by_text("Skip OTP", exact=True).click()

    time.sleep(5)