from playwright.sync_api import sync_playwright
from all_lead_creation_success.pages.talk_to_expert_page import TalkToExpertPage
from all_lead_creation_success.pages.win_product_page import WinProductPage
from all_lead_creation_success.pages.contact_form_page import ContactFormPage
from all_lead_creation_success.utils.api_helper import check_lead_created


def verify_lead(phone, source):
    if check_lead_created(phone):
        print(f"SUCCESS: Lead created from {source} for {phone}")
        return True
    else:
        print(f"FAILED: Lead NOT created from {source} for {phone}")
        return False


def test_all_lead_creation():
    phone = "9560608767"

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        page.goto("https://www.onelap.in")

        # -------- 1. Talk to Expert -------- #
        print("\nStep 1: Talk to Expert")
        talk = TalkToExpertPage(page)
        try:
            with context.expect_page(timeout=10000) as new_page_info:
                talk.submit_form(phone)
            new_page_info.value.close()
        except:
            print("No WhatsApp tab opened, checking backend...")

        page.bring_to_front()
        verify_lead(phone, "Talk to Expert")

        # -------- 2. Win Product -------- #
        print("\nStep 2: Win Product")
        win = WinProductPage(page)
        win.submit_form(phone)
        page.wait_for_timeout(3000)
        verify_lead(phone, "Win Product")

        # -------- 3. Contact Form -------- #
        print("\nStep 3: Contact Form")
        contact = ContactFormPage(page)
        contact.submit_form("Sagar", phone)
        page.wait_for_timeout(3000)
        verify_lead(phone, "Contact Form")

        browser.close()

    print("\n--- Automation Lead  Create  Completed ---")

    #pytest --html=report.html