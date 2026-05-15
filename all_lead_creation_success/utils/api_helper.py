import requests
import urllib3
import json
from datetime import datetime, timedelta  # timedelta add kiya
import time

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def check_lead_created(phone):
    url = "https://control.onelap.in/control-0.0.1-SNAPSHOT/lead/search"
    token = "Bearer Atza|eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiI2Mjk5MTM0NTA0Iiwic2NvcGVzIjpbIkFETUlOIl0sImV4cCI6MTc3NTAxNzYzMX0.p-ChhwNpfhD-5EUwf5BasPo0Obcyvk7NGwRNEosKA2wTwmUp6lVvrp23inHYTJSEyQxDuoF2WOsZFDy36NXioQ"

    headers = {
        'Authorization': token,
        'Content-Type': 'application/json; charset=utf-8',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)'
    }

    payload = {
        "phoneNumber": phone,
        "sortedBy": "DESC",
        "sortedOrder": "CREATIONDATE",
        "page": 1,
        "limit": 5
    }

    for attempt in range(2):
        try:
            response = requests.post(url, headers=headers, json=payload, verify=False, timeout=10)
            if response.status_code == 200:
                full_res = response.json()
                body = full_res.get("body", {})
                leads = body.get("leads", [])

                if leads:
                    print(f"\nTotal {len(leads)} Leads Found in Backend :")
                    print(f"{'Lead ID':<15} | {'Name':<20} | {'Creation Date':<25} | {'Stage'}")
                    print("-" * 95)

                    for lead in leads:
                        l_id = lead.get("leadId", "N/A")
                        name = lead.get("name") if lead.get("name") else "NOT_AVAILABLE"

                        # --- TIME CONVERSION LOGIC ---
                        raw_date = lead.get("creationDate", "")
                        try:
                            # UTC time ko parse karein
                            dt_utc = datetime.fromisoformat(raw_date.replace('Z', '+00:00'))
                            # IST mein convert karein (+5:30 hours)
                            dt_ist = dt_utc + timedelta(hours=5, minutes=30)
                            readable_date = dt_ist.strftime('%d/%m/%Y %I:%M %p')
                        except:
                            readable_date = raw_date[:19]  # Fallback

                        stage = lead.get("currentStage", "N/A")
                        print(f"{l_id:<15} | {name:<20} | {readable_date:<25} | {stage}")

                    return True

            time.sleep(2)
        except Exception as e:
            print(f"Error checking API: {e}")

    return False