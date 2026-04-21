
import pywhatkit
import requests
from datetime import datetime, timedelta

# -------- Date Logic -------- #
today = datetime.now()
yesterday = today - timedelta(days=1)
two_days_back = today - timedelta(days=2)

# Standard Report Dates (Yesterday - 18 March)
analytics_from = two_days_back.strftime("%Y-%m-%dT00:00:00")
analytics_to = yesterday.strftime("%Y-%m-%dT23:59:59")
search_from = yesterday.strftime("%Y-%m-%dT00:00:00")
search_to = yesterday.strftime("%Y-%m-%dT23:59:59")
report_date = yesterday.strftime("%d-%m-%Y")

# --- ACTUAL LEADS DATE --- #
actual_leads_date = (today - timedelta(days=2)).strftime("%Y-%m-%d")

# -------- SOURCE LEADS FILTER DATE -------- #
source_start = (today - timedelta(days=1)).strftime("%Y-%m-%dT00:00:00")
source_end = today.strftime("%Y-%m-%dT00:00:00")

# -------- Headers -------- #
headers = {
    "Authorization": "Bearer Atza|eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiI2Mjk5MTM0NTA0Iiwic2NvcGVzIjpbIkFETUlOIl0sImV4cCI6MTc3NTUzNjI3NH0.zrFP1GnWAbh9hdU-NviyWc9c5GkSQnGX9DOhpjGz51wLKTlZw-he7ItiYnHznB3PtN5IQvdYw0OvGShI3b_s-g",
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0"
}

# -------- API 1 : Subscription Leads (Control) -------- #
lead_url = "https://control.onelap.in/control-0.0.1-SNAPSHOT/lead/search"
lead_payload = {
    "customerType": None, "assigneeId": None, "isConverted": None, "phoneNumber": None, "state": None,
    "duration": {"from": search_from, "to": search_to},
    "labels": [{"labelId": "NGnhaf", "exist": True}],
    "page": 1, "limit": 100
}
try:
    subscription_leads = requests.post(lead_url, headers=headers, json=lead_payload).json().get("body", {}).get("count", 0)
except: subscription_leads = 0

# -------- API 2 : Analytics -------- #
analytics_url = "https://ecom.onelap.in:8443/OnelapinBackendSpring-0.0.1-SNAPSHOT/order/analytics"
analytics_payload = {
    "duration": {"from": analytics_from, "to": analytics_to},
    "type": "DEVICE", "productIds": [], "groupBy": "DAY"
}
analytics_data = requests.post(analytics_url, headers=headers, json=analytics_payload).json()
devices_agent = 0
subscription_web = 0
subscription_agent = 0
for item in analytics_data:
    if item["productType"] == "DEVICE": devices_agent += item["qbCount"]
    if item["productType"] == "SUBSCRIPTION":
        subscription_web += item["websiteCount"]
        subscription_agent += item["qbCount"]

# -------- API 3 : Order Search (Prepaid & COD) -------- #
search_url = "https://ecom.onelap.in:8443/OnelapinBackendSpring-0.0.1-SNAPSHOT/order/search/v2"
def get_order_count(mode):
    p = {"duration": {"from": search_from, "to": search_to}, "paymentMode": mode, "page": 1, "limit": 25}
    return requests.post(search_url, headers=headers, json=p).json().get("body", {}).get("items", 0)

prepaid_count = get_order_count("RAZORPAY_MAGIC_CHECKOUT")
cod_count = get_order_count("COD")

# -------- API 4 : Postman API (Actual Leads) -------- #
url_due = "https://web.onelap.in/api/utils/payments/get-due-payments"
headers_due = {"Authorization": "MTgwMDEwMzAyNzQ6YXNkcXNhZDEyIzEyMy4uMTIzMjIx", "Content-Type": "application/json"}

page, actual_leads_count = 1, 0
while True:
    payload_due = {"startDate": actual_leads_date, "endDate": actual_leads_date, "page": page, "limit": 100}
    resp = requests.post(url_due, headers=headers_due, json=payload_due)
    records = resp.json()
    if not records or resp.status_code != 200: break
    actual_leads_count += len(records)
    page += 1

# -------- API 5 : Source-wise Leads -------- #
source_url = "https://control.onelap.in/control-0.0.1-SNAPSHOT/lead/path/source-count"
source_params = {"startDate": source_start, "endDate": source_end}
source_wise_list = []
total_source_leads = 0
try:
    data_source = requests.get(source_url, headers=headers, params=source_params).json()
    if data_source.get("status") == 200 and data_source.get("body"):
        source_wise_list = data_source['body']
        total_source_leads = sum(item['count'] for item in source_wise_list)
except: pass

# --- CALCULATION LOGIC: Source Leads - Subscription Leads (Control) --- #
final_net_leads = total_source_leads - subscription_leads

# -------- Final Report -------- #
print(f"Report Date : {report_date}")
print(f"----------------------------------")
print(f"Actual number of subscriber leads : {actual_leads_count}")
print(f"Subscription Leads (Control) : {subscription_leads}")
print(f"----------------------------------")
print(f"Devices sold from agents : {devices_agent}")
print(f"Subscription sold from web : {subscription_web}")
print(f"Subscription sold from agent : {subscription_agent}")
print(f"Devices sold from web prepaid : {prepaid_count}")
print(f"Devices sold from COD : {cod_count}")

# if source_wise_list:
#     print(f"----------------------------------")
#     print(f"📊 Source-wise Leads Breakdown:")
#     for item in source_wise_list:
#         print(f"{item['source']} : {item['count']}")
#
print(f"----------------------------------")
print(f"Total Source Leads: {total_source_leads}")
print(f"Final Net Leads: {final_net_leads}")