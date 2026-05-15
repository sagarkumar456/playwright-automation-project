class LoginPage:

    def __init__(self, page):
        self.page = page

    def open(self):
        self.page.goto("https://test.onelap.in/control/")
        self.page.wait_for_timeout(5000)

    def enter_phone(self, phone):
        self.page.mouse.click(660, 480)
        self.page.wait_for_timeout(500)
        # force focus
        self.page.keyboard.press("Tab")
        self.page.wait_for_timeout(300)

        self.page.keyboard.type(phone, delay=100)

    def click_send_otp(self):
        self.page.mouse.click(660, 600)   # adjust
        self.page.wait_for_timeout(3000)

    def enter_otp(self, otp):
        # OTP field (same center area)
        self.page.mouse.click(660, 500)
        self.page.keyboard.type(otp, delay=50)
        self.page.wait_for_timeout(30000)

    def click_login(self):
        # Login button
        self.page.mouse.click(660, 600)