from playwright.sync_api import Page
import time


class AIChatPage:
    def __init__(self, page: Page):
        self.page = page
        self.bot_icon = "img.ym-icon"
        self.iframe_selector = "#ymIframe"
        self.input_selector = "#ymMsgInput"
        self.bot_msg_selector = ".ym-bot-message"

    def open_website(self):
        self.page.goto("https://test.onelap.in/")
        self.page.wait_for_load_state("networkidle")

    def click_ai_bot(self):
        self.page.wait_for_selector(self.bot_icon)
        self.page.click(self.bot_icon)
        self.page.wait_for_selector(self.iframe_selector)
        # Short sleep to let the iframe load its internal UI
        time.sleep(2)

    def get_frame(self):
        return self.page.frame_locator(self.iframe_selector)

    def send_message(self, message):
        frame = self.get_frame()
        chat_input = frame.locator(self.input_selector)
        chat_input.wait_for(state="visible")

        # Count messages BEFORE sending the new one
        current_count = frame.locator(self.bot_msg_selector).count()

        chat_input.fill(message)
        chat_input.press("Enter")
        return current_count

    def get_reply(self, previous_count):
        frame = self.get_frame()
        # Wait until the message count is higher than before
        try:
            self.page.wait_for_function(
                f"""() => {{
                    const iframe = document.querySelector('{self.iframe_selector}');
                    if (!iframe) return false;
                    const msgs = iframe.contentWindow.document.querySelectorAll('{self.bot_msg_selector}');
                    return msgs.length > {previous_count};
                }}""",
                timeout=1000
            )
            return frame.locator(self.bot_msg_selector).last.inner_text()
        except Exception:
            return "Error: AI did not reply in time."