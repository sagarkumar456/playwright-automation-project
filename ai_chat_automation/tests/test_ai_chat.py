import json
import time
from pathlib import Path
from ai_chat_automation.pages.ai_chat_page import AIChatPage
from ai_chat_automation.utils.llm_helper import get_ai_reply
from ai_chat_automation.utils.db_helper import get_otp_from_db


def test_chat_flow(page):
    # 1. Load Data
    data_path = Path(__file__).parent.parent / "data" / "messages.json"
    with open(data_path, "r", encoding="utf-8") as file:
        all_test_cases = json.load(file)

    # 2. Extract Data Dynamically
    test_case_name = "test_case_4_hardware_issue"  # Change this to test_case_1 to test the other scenario

    # Save the original scenario so we can reset it in the loop
    original_scenario = all_test_cases[test_case_name]["scenario"]
    phone_number = all_test_cases[test_case_name]["phone"]

    # 3. Setup Chat
    chat = AIChatPage(page)
    chat.open_website()
    chat.click_ai_bot()

    print("\n" + "=" * 15 + f" CHAT STARTED ({test_case_name}) " + "=" * 15 + "\n")

    ai_reply = chat.get_reply()

    # Switch to ensure OTP is only fetched and provided ONCE
    otp_already_provided = False

    # 4. Chat Loop
    for i in range(15):
        print(f"AI: {ai_reply}")

        # Reset scenario so the LLM doesn't get stuck acting like a broken record
        current_scenario = original_scenario

        # --- LIVE DB OTP LOGIC ---
        # Check if bot asks for OTP AND we haven't provided it yet
        if "otp" in ai_reply.lower() and not otp_already_provided:
            print(f"Fetching real OTP from DB for {phone_number}...")
            real_otp = get_otp_from_db(phone_number)

            if real_otp:
                current_scenario += f" [ATTENTION: The REAL OTP has arrived, it is {real_otp}. Stop waiting and reply ONLY with {real_otp} in your next message.]"
                print(f"Success: OTP Found -> {real_otp}")

                # Turn the switch ON so we don't fetch/send OTP again when bot says "login via OTP"
                otp_already_provided = True
            else:
                print("Error: OTP not found in DB!")

        # Send to LLM
        my_msg = get_ai_reply(ai_reply, current_scenario)

        print(f"Me: {my_msg}")
        print("-" * 50)

        # Send message to website
        chat.send_message(my_msg)

        # Wait 3 seconds for the website's bot to process and reply naturally
        time.sleep(3)

        # Fetch the next AI reply
        ai_reply = chat.get_reply()

        # Stop the chat if a ticket is created or verified!
        break_keywords = ["verified", "connected to an agent", "ticket has been created", "support ticket", "ticket id"]
        if any(word in ai_reply.lower() for word in break_keywords):
            break

    print(f"AI: {ai_reply}")
    print("\n" + "=" * 14 + " CHAT COMPLETED " + "=" * 14 + "\n")