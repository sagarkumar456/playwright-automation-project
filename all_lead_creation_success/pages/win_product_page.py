class WinProductPage:
    def __init__(self, page):
        self.page = page


        # We use 'exact=False' to handle extra spaces or slight text changes in the placeholder
        self.phone_input = page.get_by_placeholder("Enter your phone", exact=False).nth(1)


        self.button = page.get_by_role("button", name="Claim your reward")

    def submit_form(self, phone):
        # Wait for the section to be visible before interacting
        self.phone_input.wait_for(state="visible", timeout=10000)

        self.phone_input.click()
        self.phone_input.fill(phone)

        # Ensure the button is scrolled into view and ready for click
        self.button.scroll_into_view_if_needed()
        self.button.wait_for(state="visible")
        self.button.click()