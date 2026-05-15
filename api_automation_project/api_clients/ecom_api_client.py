# api_automation_project/api_clients/ecom_api_client.py
from api_automation_project.utils.config import BASE_URL_TEST, BASE_URL_8443, HEADERS_JSON_TOKEN_2, HEADERS_TOKEN_1

class EcomApiClient:
    def __init__(self, request_context):
        self.request = request_context

    def get_mismatched_products(self):
        response = self.request.get(
            f"{BASE_URL_TEST}/api/ecom/products/mismatchedProductPriceList",
            headers=HEADERS_TOKEN_1
        )
        return response.json()

    # We changed this function to directly accept your JSON dict
    def update_sub_item_price(self, sub_item_id: str, price_payload: dict):
        response = self.request.put(
            f"{BASE_URL_TEST}/api/ecom/product/item/sub-item/price?subItemId={sub_item_id}",
            headers=HEADERS_JSON_TOKEN_2,
            data=price_payload  # Directly passing the JSON here
        )
        return response

    def get_all_products_v2(self):
        response = self.request.get(f"{BASE_URL_8443}/products/all-v2")
        return response.json()