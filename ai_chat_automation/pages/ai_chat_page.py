from playwright.sync_api import Page


class AIChatPage:

    def __init__(self, page: Page):
        self.page = page
        self.url = "https://test.onelap.in/"
        self.bot_icon = "img.ym-icon"
        self.iframe_selector = "#ymIframe"
        self.input_selector = "#ymMsgInput"
        self.last_user_message = ""
        self.last_ai_message = ""

    # Open website
    def open_website(self):
        self.page.goto(
            self.url,
            wait_until="domcontentloaded",
            timeout=60000
        )
        self.page.wait_for_timeout(5000)

    # Open Chatbot
    def click_ai_bot(self):
        self.page.wait_for_selector(self.bot_icon)
        self.page.click(self.bot_icon)
        self.page.wait_for_timeout(5000)

    # Get iframe
    def get_frame(self):
        return self.page.frame_locator(self.iframe_selector)

    # Send User Message
    def send_message(self, message):
        self.last_user_message = message
        frame = self.get_frame()
        input_box = frame.locator(self.input_selector)
        input_box.wait_for(state="visible")
        input_box.fill(message)
        input_box.press("Enter")

    # Get Latest AI Reply (SMART WAIT)
    def get_reply(self):
        frame = self.get_frame()
        days = ["Mon ", "Tue ", "Wed ", "Thu ", "Fri ", "Sat ", "Sun "]

        # Check every 1 second, up to a maximum of 15 times (15 seconds total)
        for _ in range(15):
            self.page.wait_for_timeout(1000)

            all_texts = frame.locator("div").all_inner_texts()
            latest_ai_reply = ""

            for text in all_texts:
                text = text.strip()

                if not text or text == self.last_user_message:
                    continue
                if text in ["Powered by", "Home", "Chat"]:
                    continue

                is_timestamp = False
                for day in days:
                    if text.startswith(day):
                        is_timestamp = True
                        break
                if is_timestamp:
                    continue

                latest_ai_reply = text

            if latest_ai_reply and latest_ai_reply != self.last_ai_message:
                self.last_ai_message = latest_ai_reply
                return latest_ai_reply

        return self.last_ai_message