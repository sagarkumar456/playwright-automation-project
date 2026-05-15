import requests
from datetime import datetime, timedelta

# 👉 Auto date (Yesterday → Today)
end_date = datetime.now().date()
start_date = end_date - timedelta(days=1)

url = "https://control.onelap.in/control-0.0.1-SNAPSHOT/lead/path/count"

params = {
    "startDate": start_date.strftime("%Y-%m-%d"),
    "endDate": end_date.strftime("%Y-%m-%d"),
    "includeSubscriptionOver": "true"
}

headers = {
    "Authorization": "Bearer Atza|eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiI2Mjk5MTM0NTA0Iiwic2NvcGVzIjpbIkFETUlOIl0sImV4cCI6MTc3MzgwNzg5M30.VfhNWyXcfZozzc3pnoDof1RqhdBxYdJiY1Kg3LxaveBrZj8vNB0sVBQXdE_69oFSngdXO69v1bBM1kSDTDcDYA",
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0"
}

response = requests.get(url, headers=headers, params=params)

if response.status_code == 200:
    data = response.json()

    total = 0

    for day in data["body"]:
        for item in day["data"]:
            total += item["count"]

    print(f"Total Lead: {total}")
else:
    print("API Failed:", response.status_code)