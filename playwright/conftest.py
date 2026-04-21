import time
from idlelib.rpc import request_queue

import pytest



def pytest_addoption(parser):
    parser.addoption(
        "--browser_name", action="store", default="chrome", help="Browser Selection"
    )
    parser.addoption(
        "--url_name", action="store", default="https://rahulshettyacademy.com/client:", help="server Selection"
    )


@pytest.fixture(scope="session")
def user_credentials(request):
    return  request.param

# Pytest dekhta hai → indirect=True
#
# Value fixture me jati hai
#
# request.param me value store hoti hai
#
# Fixture return karta hai
#
# Test ko data mil jata hai

@pytest.fixture
def browserInstance(playwright,request):
    browser_name =request.config.getoption("browser_name")
    url_name = request.config.getoption("url_name")
    if browser_name == "chrome":
        browser = playwright.chromium.launch(headless=False)
    elif browser_name == "firefox":
        browser = playwright.firefox.launch(headless=False)

    context = browser.new_context()
    page = context.new_page()
    #page.goto("url_name")

    yield page
    context.close()
    browser.close()
    # headless = False → browser Showing
    # context → clean session
    # page → UI actions

