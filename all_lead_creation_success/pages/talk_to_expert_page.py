class TalkToExpertPage:

    def __init__(self, page):
        self.page = page
        self.phone_input = '#phonenumber'
        self.button = 'text=Talk to expert'

    def submit_form(self, phone):
        self.page.fill(self.phone_input, phone)
        self.page.click(self.button)