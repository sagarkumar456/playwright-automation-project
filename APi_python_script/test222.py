import requests
import json
import urllib3
from datetime import datetime

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def get_lead_data(phone_number):
    url = "https://control.onelap.in/control-0.0.1-SNAPSHOT/lead/search"

    headers = {
        'Authorization': 'Bearer Atza|eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiI2Mjk5MTM0NTA0Iiwic2NvcGVzIjpbIkFETUlOIl0sImV4cCI6MTc3NDkzMTI5M30.dI75VsjVdz8DyUM7oGK1cI6i4toD_b2Q7wuvNnAJy_6-4IXud1d1OWQoo6lingGKS4gmwXsM8RJd1nSreT7bcQ',
        'Content-Type': 'application/json; charset=utf-8',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)'
    }

    payload = {
        "phoneNumber": phone_number,
        "sortedBy": "DESC",
        "sortedOrder": "CREATIONDATE",
        "page": 1,
        "limit": 100
    }

    try:
        response = requests.post(url, headers=headers, json=payload, verify=False)

        if response.status_code == 200:
            full_res = response.json()

            # 🔥 FIX: Data extraction logic as per your JSON
            # Aapka data 'body' -> 'leads' ke andar hai
            body = full_res.get("body", {})
            leads = body.get("leads", [])

            if not leads:
                print(f"⚠️ API se leads list khali mili hai.")
                return

            print(f"\n✅ Total {len(leads)} Leads Found:")
            print(f"{'Lead ID':<12} | {'Name':<20} | {'Creation Date':<22} | {'Stage'}")
            print("-" * 85)

            for lead in leads:
                l_id = lead.get("leadId", "N/A")
                name = lead.get("name", "N/A")

                # ISO format date handling (e.g., 2026-01-21T10:30:04)
                raw_date = lead.get("creationDate", "")
                try:
                    dt_obj = datetime.fromisoformat(raw_date.replace('Z', '+00:00'))
                    readable_date = dt_obj.strftime('%d/%m/%Y %I:%M %p')
                except:
                    readable_date = raw_date[:19]  # Fallback if format differs

                stage = lead.get("currentStage", "N/A")

                print(f"{l_id:<12} | {name:<20} | {readable_date:<22} | {stage}")
        else:
            print(f"❌ Error {response.status_code}: {response.text}")

    except Exception as e:
        print(f"❌ Script Error: {e}")


if __name__ == "__main__":
    get_lead_data("9560608767")