import json
import os
from playwright.sync_api import sync_playwright
from ai_chat_automation.pages.ai_chat_page import AIChatPage


# Note: Yahan se (page) fixture hata diya hai
def test_chat_flow():
    # 1. Path setup
    current_dir = os.path.dirname(__file__)
    json_path = os.path.join(current_dir, "..", "data", "messages.json")

    with open(json_path, 'r') as f:
        data = json.load(f)
        message_list = data['chat_sequence']

    # 2. Chrome ko manually "headed" mode mein start karein
    with sync_playwright() as p:
        # headless=False se Chrome dikhayi dega
        browser = p.chromium.launch(headless=False, args=["--start-maximized"])
        context = browser.new_context(no_viewport=True)
        page = context.new_page()

        chat = AIChatPage(page)

        # 3. Steps
        chat.open_website()
        chat.click_ai_bot()

        print(f"\n--- Starting Chat Sequence ---")

        for msg in message_list:
            print(f"Me: {msg}")
            count_before = chat.send_message(msg)
            reply = chat.get_reply(count_before)
            print(f"AI: {reply}")
            print("-" * 20)

        browser.close()

        #pytest --html=report.html