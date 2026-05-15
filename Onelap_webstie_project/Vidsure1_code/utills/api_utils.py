class ApiUtils:
    def __init__(self, page):
        self.page = page
        self.crm_url = "https://test.onelap.in/api/ecom/order/search/v2"
        self.crm_token = "Bearer Atza|eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiI2Mjk5MTM0NTA0Iiwic2NvcGVzIjpbIkFETUlOIiwiTU9ERVJBVE9SIl0sImV4cCI6MTc3ODMwNDA2OX0.G6i6JTaw0IHXQwwCyR9Vo1F4XKcBKmmpN0AOP5BUQ7xSlAx2qauRGA5MaknfO7CBUD3otRNUzFABGMg-vQ20DQ"


    # FUNCTION 1: Intercept API from UI

    def capture_payment_from_ui(self, ui_click_action):
        """
        Yeh function UI ke click ka wait karega aur background me 
        'on-successful-payment' API se data nikal lega.
        """
        with self.page.expect_request("**/api/ecom/magic-checkout/on-successful-payment") as request_info:
            # Yahan hum UI wala button click execute karwa rahe hain
            ui_click_action()

        success_request = request_info.value
        post_data = success_request.post_data_json

        # Payment ID return kar rahe hain
        return post_data.get("razorpay_payment_id")


    # FUNCTION 2: Check Order in CRM

    def check_order_in_Control(self, payment_id: str, phone_number: str):
        payload = {
            "duration": None, "orderedSimSerialNumber": None, "orderedSubscriptionDeviceImei": None,
            "serialNumberInRelatedTo": None, "fastDelivery": None, "status": None, "awbNumber": None,
            "paymentMode": None, "isShippableButUnshipped": None, "replacementImei": None,
            "paymentId": payment_id,
            "productIds": [], "reverseOrder": None, "pgOrderId": None, "sortedBy": "DESC",
            "aggregatorName": None, "phoneNumber": phone_number, "orderState": None,
            "page": 1, "limit": 25, "orderId": None, "isScanned": None, "isPrinted": None,
            "isMCF": None, "isDispatched": None
        }

        response = self.page.request.post(
            self.crm_url,
            headers={
                "authorization": self.crm_token,
                "content-type": "application/json; charset=utf-8"
            },
            data=payload
        )

        assert response.ok, f"CRM API Call Failed with status: {response.status}"
        return response.json()