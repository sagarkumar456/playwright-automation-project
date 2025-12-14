# from playwright.sync_api import Page
#
# # def test_playwrightBasic(playwright):
# #     browser = playwright.chromium.launch(headless=False)
# #     context = browser.new_context()
# #     page = context.new_page()
# #     page.goto("https://www.onelap.in/")
#
# def test_playwright(playwright):
#     browser=playwright.chromium.launch(headless=False)
#     context = browser.new_context()
#     page = context.new_page()
#     page.goto("https://www.copystar.in/")
#
# def test_PlaywrightShortCut(page: Page):
# #     page.goto("https://www.copystar.in/")
import time
from tabnanny import check

from playwright.sync_api import Page, expect


def test_locators(page: Page):
    page.goto("https://rahulshettyacademy.com/loginpagePractise/")
    page.get_by_label("Username:").fill("rahulshettyacademy") # Fill Username + Password
    page.get_by_label("Password:").fill("learning4324234")# Select Teacher in dropdown
    # Select Student (checkbox enabled)
    page.get_by_role("combobox").select_option("teach")
    # Now checkbox will work
    page.locator("#terms").check()
    page.get_by_role("link",name="terms and conditions").click()
    page.get_by_role("button",name="Sign In").click()
    expect(page.get_by_text("Incorrect username/password")).to_be_visible() #show the validation error

    #Incorrect username/password. assertions
time.sleep(5)


from playwright.async_api import Playwright
#How to Open browser Firefox
def  test_FireFoxBrowser(playwright: Playwright):
    browser = playwright.firefox.launch(headless=False)
    page = browser.new_page()
    page.goto("https://rahulshettyacademy.com/loginpagePractise/")
    page.get_by_label("Username:").fill("rahulshettyacademy")  # Fill Username + Password
    page.get_by_label("Password:").fill("learning")  # Select Teacher in dropdown
    # Select Student (checkbox enabled)
    page.get_by_role("combobox").select_option("teach")
    # Now checkbox will work
    page.locator("#terms").check()
    page.get_by_role("link", name="terms and conditions").click()
    page.get_by_role("button", name="Sign In").click()
    time.sleep(40)






# def test_onelapLoginPage(page: Page):
#     page.goto("https://www.onelap.in/login")
#     page.get_by_label("Enter Mobile Number").fill("6299134504")
#     page.get_by_role("button",name="Send Otp").click()
#     time.sleep(5)

# def test_elementalselenium(page: Page):
#
#     page.goto("https://the-internet.herokuapp.com/")
#     page.get_by_role("link", name="Forgot Password").click()
#     page.get_by_label("E-mail").fill("skdas1641999@gmail.com")
#
#     # Api
#     with page.expect_response("**/forgot_password") as resp_info:
#         page.get_by_role("button", name="Retrieve password").click()
#
#     # API RESPONSE
#     response = resp_info.value
#     print("Status Code:", response.status)
#
#     # ASSERTION (FAIL if NOT 200)
#     assert response.status == 200, f"API FAILED! Status = {response.status}"
#
#     time.sleep(3)


# def test_lambdatest(page: Page):
#     page.goto("https://www.lambdatest.com/selenium-playground/")
#     page.get_by_role("link",name="Ajax Form Submit").click()
#     page.locator("#title").fill("Sagar")
#     page.locator("#description").fill("Hi bro, how are you?")
#     #api response
#     with page.expect_response("**/simple-form-demo.php") as resp:
#         page.get_by_role("button", name="submit").click()
#
#     response = resp.value
#     print("response value:",response.status)  # 404
#
#     time.sleep(5)


