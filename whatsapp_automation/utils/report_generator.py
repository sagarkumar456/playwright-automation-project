import requests
from datetime import datetime, timedelta

def generate_report():

    today = datetime.now()
    yesterday = today - timedelta(days=1)
    two_days_back = today - timedelta(days=2)

    # Dates
    analytics_from = two_days_back.strftime("%Y-%m-%dT00:00:00")
    analytics_to = yesterday.strftime("%Y-%m-%dT23:59:59")
    search_from = yesterday.strftime("%Y-%m-%dT00:00:00")
    search_to = yesterday.strftime("%Y-%m-%dT23:59:59")
    report_date = yesterday.strftime("%d-%m-%Y")

    actual_leads_date = (today - timedelta(days=2)).strftime("%Y-%m-%d")

    source_start = (today - timedelta(days=1)).strftime("%Y-%m-%dT00:00:00")
    source_end = today.strftime("%Y-%m-%dT00:00:00")

    headers = {
        "Authorization": "Bearer Atza|eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiI2Mjk5MTM0NTA0Iiwic2NvcGVzIjpbIkFETUlOIl0sImV4cCI6MTc3ODMwMTcyNn0.r4-NEY7My3NcC5Y4xYZoFEiaPLnC2TRpg-i2C3zYv_dtl0M_HEcrTVNkN5xAKZwmHzE6ASsmOVjLBvStbTkEnQ",
        "Content-Type": "application/json"
    }

    # -------- API 1 : Subscription Leads -------- #
    lead_url = "https://control.onelap.in/control-0.0.1-SNAPSHOT/lead/search"
    lead_payload = {
        "duration": {"from": search_from, "to": search_to},
        "labels": [{"labelId": "NGnhaf", "exist": True}],
        "page": 1,
        "limit": 100
    }

    try:
        subscription_leads = requests.post(lead_url, headers=headers, json=lead_payload).json().get("body", {}).get("count", 0)
    except:
        subscription_leads = 0

    # -------- API 2 : Analytics -------- #
    analytics_url = "https://ecom.onelap.in:8443/OnelapinBackendSpring-0.0.1-SNAPSHOT/order/analytics"
    analytics_payload = {
        "duration": {"from": analytics_from, "to": analytics_to},
        "type": "DEVICE",
        "productIds": [],
        "groupBy": "DAY"
    }

    devices_agent = 0
    subscription_web = 0
    subscription_agent = 0

    try:
        analytics_data = requests.post(analytics_url, headers=headers, json=analytics_payload).json()

        for item in analytics_data:
            if item["productType"] == "DEVICE":
                devices_agent += item["qbCount"]

            if item["productType"] == "SUBSCRIPTION":
                subscription_web += item["websiteCount"]
                subscription_agent += item["qbCount"]
    except:
        pass

    # -------- API 3 : Order Search -------- #
    search_url = "https://ecom.onelap.in:8443/OnelapinBackendSpring-0.0.1-SNAPSHOT/order/search/v2"

    def get_order_count(mode):
        payload = {
            "duration": {"from": search_from, "to": search_to},
            "paymentMode": mode,
            "page": 1,
            "limit": 25
        }
        try:
            return requests.post(search_url, headers=headers, json=payload).json().get("body", {}).get("items", 0)
        except:
            return 0

    prepaid_count = get_order_count("RAZORPAY_MAGIC_CHECKOUT")
    cod_count = get_order_count("COD")

    # -------- API 4 : Actual Leads -------- #
    url_due = "https://web.onelap.in/api/utils/payments/get-due-payments"
    headers_due = {
        "Authorization": "MTgwMDEwMzAyNzQ6YXNkcXNhZDEyIzEyMy4uMTIzMjIx",
        "Content-Type": "application/json"
    }

    actual_leads_count = 0
    page = 1

    while True:
        payload_due = {
            "startDate": actual_leads_date,
            "endDate": actual_leads_date,
            "page": page,
            "limit": 100
        }

        try:
            resp = requests.post(url_due, headers=headers_due, json=payload_due)

            if resp.status_code != 200:
                break

            records = resp.json()
            if not records:
                break

            actual_leads_count += len(records)
            page += 1

        except:
            break

    # -------- API 5 : Source Leads -------- #
    source_url = "https://control.onelap.in/control-0.0.1-SNAPSHOT/lead/path/source-count"
    params = {"startDate": source_start, "endDate": source_end}

    total_source_leads = 0

    try:
        data = requests.get(source_url, headers=headers, params=params).json()
        if data.get("body"):
            total_source_leads = sum(i["count"] for i in data["body"])
    except:
        pass

    # -------- Final Calculation -------- #
    final_net_leads = total_source_leads - subscription_leads

    # -------- Final Message -------- #
    message = f"""📊 Automated Daily Report : {report_date}
----------------------------------
Actual number of subscriber leads : {actual_leads_count}
Subscription Leads (Control) : {subscription_leads}
----------------------------------
Devices sold from agents : {devices_agent}
Subscription sold from web : {subscription_web}
Subscription sold from agent : {subscription_agent}
Devices sold from web prepaid : {prepaid_count}
Devices sold from COD : {cod_count}
----------------------------------
Total Source Leads: {total_source_leads}
Final Device  Net Leads: {final_net_leads}
"""

    return message