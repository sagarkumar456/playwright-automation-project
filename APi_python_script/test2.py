import requests

url = "https://ecom.onelap.in:8443/OnelapinBackendSpring-0.0.1-SNAPSHOT/order/analytics"

headers = {
    "Authorization": "Bearer Atza|eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiI2Mjk5MTM0NTA0Iiwic2NvcGVzIjpbIkFETUlOIl0sImV4cCI6MTc3MzcyMTI4Mn0.hJiQF5qmZoWkhpO_iwX2u9OPUOllrjwDTGd7gnaRSWqYbK-JEots3mUS_bvr8syp7GExj65De9t_0iawEDgERg",
    "Content-Type": "application/json"
}

payload = {
    "duration": {
        "from": "2026-03-14T00:00:00",
        "to": "2026-03-15T23:59:59"
    },
    "type": "DEVICE",
    "productIds": [],
    "groupBy": "DAY"
}

response = requests.post(url, headers=headers, json=payload)

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

print(f"Devices sold from agents : {devices_agent}")
print(f"Subscription sold from web : {subscription_web}")
print(f"Subscription sold from agent : {subscription_agent}")