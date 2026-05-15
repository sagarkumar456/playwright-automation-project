import time
from calendar import firstweekday

from playwright.sync_api import Page, Playwright, expect

from utills.apiBase import APIUtils


#api call from the browser -> api call contact server return back response to browser -> browser use response to generate html (data)


def intercept_response(route, request):
    route.continue_(url="https://rahulshettyacademy.com/api/ecom/order/get-orders-details?id=6940edb732ed865871367533")

def test_Network(page: Page):
    page.route("https://rahulshettyacademy.com/api/ecom/order/get-orders-details?id=*",intercept_response)

    page.goto("https://rahulshettyacademy.com/client")
    page.get_by_placeholder("email@example.com").fill("skdas1641999@gmail.com")
    page.get_by_placeholder("enter your passsword").fill("Sagardas456")
    page.get_by_role("button", name="login").click()
    page.get_by_role("button", name="ORDERS").click()
    page.get_by_role("button", name="View").first.click()
    message = page.locator(".blink_me").text_content()
    print(message)
    time.sleep(5)



#login without username  and password  ->got Home Page -> click on Order section -> (Your Orders) present there


def test_session_storage(playwright: Playwright):
    apiutils =APIUtils()
    getToken = apiutils.getToken(playwright)
    browser = playwright.chromium.launch(headless=False)
    page = browser.new_page()
    #SCRIPT to inject token in session local storage
    page.add_init_script(f"""localStorage.setItem('token','{getToken}')""")
    page.goto("https://rahulshettyacademy.com/client")
    page.get_by_role("button", name="ORDERS").click()
    expect(page.get_by_text('Your Orders')).to_be_visible()
    time.sleep(5)





