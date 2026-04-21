class ContactFormPage:

    def __init__(self, page):
        self.page = page

        self.name = 'input[placeholder="Enter your name"]'
        self.phone = '#number'   # updated locator
        self.dropdown = 'select'
        self.message = 'textarea'
        self.submit = 'button:has-text("Submit")'

    def submit_form(self, name, phone):
        self.page.wait_for_selector(self.phone)

        self.page.fill(self.name, name)
        self.page.fill(self.phone, phone)

        self.page.select_option(self.dropdown, label="Sales")
        self.page.fill(self.message, "Automation Testing Lead")

        self.page.click(self.submit)