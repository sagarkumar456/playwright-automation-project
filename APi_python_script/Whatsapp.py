import requests
from datetime import datetime, timedelta

# ==========================================================
# 1. WATI CONFIGURATION (Personal Number)
# ==========================================================
# Screenshot se 'Access Token' pura copy karke yahan paste karein
WATI_ACCESS_TOKEN = "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1bmlxdWVfbmFtZSI6ImpheWFudEBvbmVsYXAuaW4iLCJuYW1laWQiOiJqYXlhbnRAb25lbGFwLmluIiwiZW1haWwiOiJqYXlhbnRAb25lbGFwLmluIiwiYXV0aF90aW1lIjoiMDMvMjAvMjAyNiAwNToxNzozNyIsInRlbmFudF9pZCI6IjEwODY5IiwiZGJfbmFtZSI6Im10LXByb2QtVGVuYW50cyIsImh0dHA6Ly9zY2hlbWFzLm1pY3Jvc29mdC5jb20vd3MvMjAwOC8wNi9pZGVudGl0eS9jbGFpbXMvcm9sZSI6IkFETUlOSVNUUkFUT1IiLCJleHAiOjI1MzQwMjMwMDgwMCwiaXNzIjoiQ2xhcmVfQUkiLCJhdWQiOiJDbGFyZV9BSSJ9.Kj3BQ80t3cpqez1QM4Hjlp4Ftlj2vEymrUt0mRjf9IwE"

# Aapka naya Wati API Endpoint
WATI_BASE_URL = "https://live-10869.wati.io/10869"

# Apna WhatsApp number (91 ke sath)
MY_PHONE_NUMBER = "916299134504"

# ==========================================================
# 2. DATE LOGIC
# ==========================================================
today = datetime.now()
yesterday = today - timedelta(days=1)
two_days_back = today - timedelta(days=2)

report_date = yesterday.strftime("%d-%m-%Y")
analytics_from = two_days_back.strftime("%Y-%m-%dT00:00:00")
analytics_to = yesterday.strftime("%Y-%m-%dT23:59:59")
search_from = yesterday.strftime("%Y-%m-%dT00:00:00")
search_to = yesterday.strftime("%Y-%m-%dT23:59:59")

actual_leads_date = (today - timedelta(days=2)).strftime("%Y-%m-%d")
source_start = (today - timedelta(days=1)).strftime("%Y-%m-%dT00:00:00")
source_end = today.strftime("%Y-%m-%dT00:00:00")

# ==========================================================
# 3. ONELAP HEADERS & API CALLS (Data Fetching)
# ==========================================================
headers = {
    "Authorization": "Bearer Atza|eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiI2Mjk5MTM0NTA0Iiwic2NvcGVzIjpbIkFETUlOIl0sImV4cCI6MTc3NDA2NzMxNX0._F6OWk-VRNnANl7ftHIAoBTKndJnvxsbMr5LaRjek8Ztukok1J7_4mq49aB6Jb8RT1YTFUKgP1j7j_81JQR1rw",
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0"
}

# --- Data Fetching Logic ---
try:
    # Subscription Leads
    lead_url = "https://control.onelap.in/control-0.0.1-SNAPSHOT/lead/search"
    lead_payload = {"customerType": None, "duration": {"from": search_from, "to": search_to},
                    "labels": [{"labelId": "NGnhaf", "exist": True}], "page": 1, "limit": 100}
    subscription_leads = requests.post(lead_url, headers=headers, json=lead_payload).json().get("body", {}).get("count",
                                                                                                                0)

    # Analytics
    analytics_url = "https://ecom.onelap.in:8443/OnelapinBackendSpring-0.0.1-SNAPSHOT/order/analytics"
    analytics_payload = {"duration": {"from": analytics_from, "to": analytics_to}, "type": "DEVICE", "productIds": [],
                         "groupBy": "DAY"}
    analytics_data = requests.post(analytics_url, headers=headers, json=analytics_payload).json()
    devices_agent, subscription_web, subscription_agent = 0, 0, 0
    for item in analytics_data:
        if item["productType"] == "DEVICE": devices_agent += item["qbCount"]
        if item["productType"] == "SUBSCRIPTION":
            subscription_web += item["websiteCount"]
            subscription_agent += item["qbCount"]

    # Order Search (Prepaid/COD)
    search_url = "https://ecom.onelap.in:8443/OnelapinBackendSpring-0.0.1-SNAPSHOT/order/search/v2"
    prepaid_count = requests.post(search_url, headers=headers, json={"duration": {"from": search_from, "to": search_to},
                                                                     "paymentMode": "RAZORPAY_MAGIC_CHECKOUT",
                                                                     "page": 1, "limit": 25}).json().get("body",
                                                                                                         {}).get(
        "items", 0)
    cod_count = requests.post(search_url, headers=headers,
                              json={"duration": {"from": search_from, "to": search_to}, "paymentMode": "COD", "page": 1,
                                    "limit": 25}).json().get("body", {}).get("items", 0)

    # Actual Leads (Due Payments)
    url_due = "https://web.onelap.in/api/utils/payments/get-due-payments"
    headers_due = {"Authorization": "MTgwMDEwMzAyNzQ6YXNkcXNhZDEyIzEyMy4uMTIzMjIx", "Content-Type": "application/json"}
    actual_leads_count = 0
    resp_due = requests.post(url_due, headers=headers_due,
                             json={"startDate": actual_leads_date, "endDate": actual_leads_date, "page": 1,
                                   "limit": 100}).json()
    actual_leads_count = len(resp_due) if isinstance(resp_due, list) else 0

    # Source-wise Leads
    source_url = "https://control.onelap.in/control-0.0.1-SNAPSHOT/lead/path/source-count"
    data_source = requests.get(source_url, headers=headers,
                               params={"startDate": source_start, "endDate": source_end}).json()
    total_source_leads = sum(item['count'] for item in data_source.get("body", []))

    final_net_leads = total_source_leads - subscription_leads

except Exception as e:
    print(f"Data Fetching Error: {e}")
    subscription_leads = actual_leads_count = devices_agent = subscription_web = subscription_agent = prepaid_count = cod_count = total_source_leads = final_net_leads = 0

# ==========================================================
# 4. MESSAGE FORMATTING
# ==========================================================
whatsapp_msg = f"""*🚀 DAILY AUTOMATION REPORT*
*Date:* {report_date}
----------------------------------
*Actual leads (Subscriber):* {actual_leads_count}
*Control Leads (Subscription):* {subscription_leads}
----------------------------------
*Devices (Agent):* {devices_agent}
*Sub (Web):* {subscription_web}
*Sub (Agent):* {subscription_agent}
*Prepaid Orders:* {prepaid_count}
*COD Orders:* {cod_count}
----------------------------------
*Total Source Leads:* {total_source_leads}
*Final Net Leads (Source - Control):* {final_net_leads}"""


# ==========================================================
# 5. WATI SEND FUNCTION (405 Error Fix)
# ==========================================================
def send_to_wati(msg):
    # Endpoint for session message
    url = f"{WATI_BASE_URL}/api/v1/sendSessionMessage/{MY_PHONE_NUMBER}"

    headers_wati = {
        "Authorization": WATI_ACCESS_TOKEN,  # Isme 'Bearer ' hona zaroori hai
        "Content-Type": "application/json"
    }

    # Naye servers par GET request with params zyada stable chalti hai
    params = {"messageText": msg}

    try:
        # POST ki jagah GET try kar rahe hain 405 fix karne ke liye
        response = requests.get(url, headers=headers_wati, params=params)

        # Agar GET fail ho (405 de), toh automatically POST try karega
        if response.status_code == 405:
            response = requests.post(url, headers=headers_wati, params=params)

        if response.status_code == 200:
            print(f"✅ Report aapke number ({MY_PHONE_NUMBER}) par bhej di gayi hai!")
        else:
            print(f"❌ Wati Error: {response.status_code}")
            print(f"Details: {response.text}")

    except Exception as e:
        print(f"❌ Connection Error: {e}")


# --- TRIGGER ---
print(whatsapp_msg)
send_to_wati(whatsapp_msg)