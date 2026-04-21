from playwright.sync_api import Page

class WhatsAppPage:

    def __init__(self, page: Page):
        self.page = page

    def open_whatsapp(self):
        self.page.goto("https://web.whatsapp.com/")
        self.page.wait_for_timeout(15000)  # QR login time

    def search_group(self, group_name):
        # exact search input using placeholder (100% stable)
        search_box = self.page.get_by_placeholder("Search or start a new chat")

        search_box.wait_for(state="visible", timeout=60000)
        search_box.click()
        search_box.fill(group_name)

        # wait for group
        self.page.get_by_title(group_name).wait_for(timeout=30000)

        # click group
        self.page.get_by_title(group_name).click()

    def send_message(self, message):
        message_box = self.page.locator("//footer//div[@contenteditable='true']")

        message_box.wait_for(state="visible", timeout=30000)
        message_box.click()
        message_box.fill(message)

        message_box.press("Enter")