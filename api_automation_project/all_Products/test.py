import requests
import urllib3
import json

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

url = "https://test.onelap.in:8443/OnelapinBackendSpring-0.0.1-SNAPSHOT/products/all-v2"

response = requests.get(url, verify=False)
data = response.json()

search_text = "ol_micro_plus_3_a"

found = False

total_mrp = 0
total_offer_price = 0

print("Status Code:", response.status_code)


def extract_prices(obj):

    global found, total_mrp, total_offer_price

    if isinstance(obj, dict):

        # check match condition
        match = False

        for key, value in obj.items():

            if isinstance(value, str) and search_text.lower() in value.lower():
                match = True
                found = True

            # recursive call
            extract_prices(value)

        # if matched object → extract price fields
        if match:

            # try common keys (API depends on naming)
            mrp_keys = ["mrp", "MRP", "price", "originalPrice", "listPrice"]
            offer_keys = ["offerPrice", "offer_price", "sellingPrice", "salePrice"]

            for k, v in obj.items():

                if k in mrp_keys and isinstance(v, (int, float, str)):
                    try:
                        total_mrp += float(v)
                    except:
                        pass

                if k in offer_keys and isinstance(v, (int, float, str)):
                    try:
                        total_offer_price += float(v)
                    except:
                        pass

    elif isinstance(obj, list):
        for item in obj:
            extract_prices(item)


extract_prices(data)

print("\n========== RESULT ==========")

if found:
    print("Search Item Found:", search_text)
    print("TOTAL MRP        :", total_mrp)
    print("TOTAL OFFER PRICE:", total_offer_price)
    print("FINAL TOTAL      :", total_mrp + total_offer_price)
else:
    print(f"'{search_text}' data nahi mila")