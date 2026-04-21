# This test case validates the product-adding functionality on the shopping application.
#
# First, the script opens the login page and enters valid credentials. It selects the appropriate user type from the dropdown, accepts the terms and conditions, and clicks on the Sign-In button.
#
# After successfully logging in, the test navigates to the shop page where two specific products—iPhone X and Nokia Edge—are added to the cart.
#
# Next, the script clicks on the Checkout button to open the cart page.
#
# On the checkout page, the test verifies that exactly two items are displayed.
# This confirms that both selected products were added to the cart correctly and that the cart functionality is working as expected.

import time

from playwright.sync_api import Page, expect


def test_UiValidation(page:Page):
    #iphone X Nokia Edge --> verify two item showing in cart
    page.goto("https://rahulshettyacademy.com/loginpagePractise/")
    page.get_by_label("Username:").fill("rahulshettyacademy")
    page.get_by_label("Password:").fill("learning")
    page.get_by_role("combobox").select_option("teach")#select the dropdown option
    page.locator("#terms").click()
    page.get_by_role("link",name="terms and conditions").click()
    page.get_by_role("button",name="Sign In").click()
    iphoneProduct = page.locator("app-card").filter(has_text="iphone X")
    iphoneProduct.get_by_role("button").click()
    NokiaEdgeProduct = page.locator("app-card").filter(has_text="Nokia Edge")
    NokiaEdgeProduct.get_by_role("button").click()
    #Next step After adding two products, I want to verify on the checkout page whether both products were added or not.
    page.get_by_text("Checkout").click()
    expect(page.locator(".media-body")).to_have_count(2)

    time.sleep(5)



def test_childWindowHandel(page:Page):
    page.goto("https://rahulshettyacademy.com/loginpagePractise/")

    with page.expect_popup() as newPage_info:
    #step1
    #step2
        page.locator(".blinkingText").click()
        child_page = newPage_info.value
        text = child_page.locator(".red").text_content()
        print(text)
        words = text.split("at")
        email = words[1].strip().split(" ")[0]
        assert email== "mentor@rahulshettyacademy.com"
        time.sleep(5)

