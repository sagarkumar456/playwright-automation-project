import requests
from datetime import datetime, timedelta

# -------- Date Logic -------- #

today = datetime.now()

yesterday = today - timedelta(days=1)
two_days_back = today - timedelta(days=2)

analytics_from = two_days_back.strftime("%Y-%m-%dT00:00:00")
analytics_to = yesterday.strftime("%Y-%m-%dT23:59:59")

search_from = yesterday.strftime("%Y-%m-%dT00:00:00")
search_to = yesterday.strftime("%Y-%m-%dT23:59:59")

report_date = yesterday.strftime("%d-%m-%Y")

# -------- Headers -------- #

headers = {
    "Authorization": "Bearer Atza|eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiI2Mjk5MTM0NTA0Iiwic2NvcGVzIjpbIkFETUlOIl0sImV4cCI6MTc3MzgwNzg5M30.VfhNWyXcfZozzc3pnoDof1RqhdBxYdJiY1Kg3LxaveBrZj8vNB0sVBQXdE_69oFSngdXO69v1bBM1kSDTDcDYA",
    "Content-Type": "application/json"
}

# -------- API 1 : Analytics -------- #

analytics_url = "https://ecom.onelap.in:8443/OnelapinBackendSpring-0.0.1-SNAPSHOT/order/analytics"

analytics_payload = {
    "duration": {
        "from": analytics_from,
        "to": analytics_to
    },
    "type": "DEVICE",
    "productIds": [],
    "groupBy": "DAY"
}

response = requests.post(analytics_url, headers=headers, json=analytics_payload)
data = response.json()

devices_agent = 0
subscription_web = 0
subscription_agent = 0

for item in data:

    if item["productType"] == "DEVICE":
        devices_agent += item["qbCount"]

    if item["productType"] == "SUBSCRIPTION":
        subscription_web += item["websiteCount"]
        subscription_agent += item["qbCount"]

# -------- API 2 : Order Search -------- #

search_url = "https://ecom.onelap.in:8443/OnelapinBackendSpring-0.0.1-SNAPSHOT/order/search/v2"

search_payload = {
    "duration": {
        "from": search_from,
        "to": search_to
    },
    "paymentMode": "RAZORPAY_MAGIC_CHECKOUT",
    "page": 1,
    "limit": 25,
    "sortedBy": "DESC"
}

response = requests.post(search_url, headers=headers, json=search_payload)
data = response.json()

prepaid_count = data.get("body", {}).get("items", 0)

# -------- COD -------- #

search_payload["paymentMode"] = "COD"

response = requests.post(search_url, headers=headers, json=search_payload)
data = response.json()

cod_count = data.get("body", {}).get("items", 0)

# -------- Final Report -------- #

print(f"Date : {report_date}")
print(f"Devices sold from agents : {devices_agent}")
print(f"Subscription sold from web : {subscription_web}")
print(f"Subscription sold from agent : {subscription_agent}")
print(f"Devices sold from web prepaid : {prepaid_count}")
print(f"Devices sold from COD : {cod_count}")