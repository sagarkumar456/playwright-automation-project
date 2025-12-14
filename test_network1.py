from playwright.sync_api import Page
#api call from browser -> api call contact server return back response to browser -> browser use response to generate html (data)

fakePayLoadOrderResponse = {
    "data": [],
    "message": "No Orders"
}

def intercept_response(route, request):
    route.fulfill(
        json=fakePayLoadOrderResponse
    )

def test_Network(page: Page):
    page.route("https://rahulshettyacademy.com/api/ecom/order/get-orders-for-customer/*",intercept_response)

    page.goto("https://rahulshettyacademy.com/client/#/auth/login")
    page.get_by_placeholder("email@example.com").fill("skdas1641999@gmail.com")
    page.get_by_placeholder("enter your passsword").fill("Sagardas456")
    page.get_by_role("button", name="login").click()
    page.get_by_role("button", name="ORDERS").click()

    order_text = page.locator(".mt-4").text_content()
    print(order_text)
