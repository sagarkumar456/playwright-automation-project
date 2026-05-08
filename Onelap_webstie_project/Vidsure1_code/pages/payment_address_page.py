class AddressPage:
    def __init__(self, page):
        self.page = page

        #  Correct iframe (Razorpay)
        self.frame = page.frame_locator(".razorpay-checkout-frame")

        self.pincode_input = self.frame.get_by_placeholder("Pincode")
        self.full_name_input = self.frame.get_by_placeholder("Full name")
        self.house_input = self.frame.locator("#line1")
        self.area_input = self.frame.locator("#line2")
        self.continue_btn = self.frame.locator('button[name="new_shipping_address_cta"]')

    def fill_address_details(self, pincode, name, house, area):
        self.pincode_input.wait_for(state="visible")
        self.pincode_input.fill(pincode)
        self.pincode_input.press("Tab")

        self.full_name_input.fill(name)
        self.house_input.fill(house)

        # Area input
        self.area_input.fill(area)

        # wait for suggestion list
        suggestions = self.frame.locator("div:has-text('Patna')")

        suggestions.first.wait_for()

        #  FIRST suggestion
        suggestions.first.click()

    def click_continue(self):
        self.continue_btn.click()
        

