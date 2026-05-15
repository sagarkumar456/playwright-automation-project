import time

from playwright.sync_api import Playwright, expect

from utills.apiBase import APIUtils


def test_e2n_web_api(playwright: Playwright):
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()


    #create order->create id
    API_utils=APIUtils()
    orderId =API_utils.createOrder(playwright)

    #login
    page.goto("https://rahulshettyacademy.com/client/#/auth/login")
    page.get_by_placeholder("email@example.com").fill("skdas1641999@gmail.com")
    page.get_by_placeholder("enter your passsword").fill("Sagardas456")
    page.get_by_role("button",name="login").click()

    page.get_by_role("button", name="ORDERS").click()


    #order history-> Order is present
    row = page.locator("tr").filter(has_text=orderId)
    row.get_by_role("button", name="View").click()

    expect(page.locator(".tagline")).to_contain_text("Thank you for Shopping With Us")

    context.close()



