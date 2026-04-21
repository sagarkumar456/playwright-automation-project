from playwright.sync_api import sync_playwright
from whatsapp_automation.pages.whatsapp_page import WhatsAppPage
from whatsapp_automation.utils.report_generator import generate_report


def test_send_whatsapp_report():

    message = generate_report()

    with sync_playwright() as p:
        browser = p.chromium.launch_persistent_context(
            user_data_dir="user_data",
            headless=False
        )

        page = browser.new_page()

        whatsapp = WhatsAppPage(page)

        # Step 1: Open WhatsApp
        whatsapp.open_whatsapp()

        # Step 2: Search Group
        whatsapp.search_group("Daily Sales Report - Onelap")

        # Step 3: Wait after selecting group (IMPORTANT)
        page.wait_for_timeout(3000)

        # Step 4: Send Message
        whatsapp.send_message(message)

        print("Automated Daily Report  Message Sent Successfully")

        # Step 5: Wait before closing
        page.wait_for_timeout(5000)

        browser.close()

        #pytest --html=report.html