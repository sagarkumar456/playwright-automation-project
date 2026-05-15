class KotakBankPage:
    def __init__(self, page):
        self.page = page
        self.frame = page.frame_locator(".razorpay-checkout-frame")

        self.netbanking_option = self.frame.get_by_text("Netbanking")
        self.kotak_bank_option = self.frame.get_by_role(
            "button", name="Kotak Mahindra Bank"
        ).first

    def select_kotak_bank(self):
        self.netbanking_option.click()

        self.kotak_bank_option.wait_for(state="visible")

        with self.page.expect_popup() as popup_info:
            self.kotak_bank_option.click()

        self.razorpay_popup = popup_info.value

    def click_success(self):
        success_button = self.razorpay_popup.locator("button.success")
        success_button.wait_for(state="visible")
        success_button.click()