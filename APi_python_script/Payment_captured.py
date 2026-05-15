import requests

url = "https://ecom.onelap.in:8443/OnelapinBackendSpring-0.0.1-SNAPSHOT/payment/capture-by-payment-id"

headers = {
    "Authorization": "Bearer Atza|eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiI2Mjk5MTM0NTA0Iiwic2NvcGVzIjpbIkFETUlOIl0sImV4cCI6MTc3MTA0NDU5OX0.FzWY2pC8mvR4VEgzc7gKe0Da1WPe7d3OZwYfnWLsRkYSX_daKimZ66I5anMxGt6_ncg48PkfNkSuXOfkfPc_OQ",
    "Content-Type": "application/json"
}

payload = ["pay_SEpXfIKBMhnHIH"]

response = requests.post(url, headers=headers, json=payload)

if response.status_code == 200:
    print(f"Payment captured successfully: {payload[0]}")
else:
    print(" Capture Failed")
    print("Status:", response.status_code)
    print("Response:", response.text)
