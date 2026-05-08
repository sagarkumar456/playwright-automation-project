import pytest

from playwright.sync_api import sync_playwright

@pytest.fixture(scope="function")
def page():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        yield page
        browser.close()




# A fixture in pytest is simply a reusable setup function that prepares data or resources for your tests.

# 1. @pytest.fixture(scope="function")
# Defines a fixture named page
# scope="function" means:
# A new browser will open for every test function


# 2. sync_playwright()
# Starts the Playwright engine
# Gives access to browsers (Chromium, Firefox, WebKit)


# 3. browser = p.chromium.launch(headless=False)
# Launches the browser
# headless=False → UI is visible (useful for debugging)

# 4. context = browser.new_context()
# Creates a new isolated browser session
# No shared cookies/cache

# 5. page = context.new_page()
# Opens a new tab (page)

# 6. yield page
#
# This is the most important part:
#
# Sends the page object to your test
# Pauses here while the test runs
#
# Example:
#
# def test_google(page):
#     page.goto("https://google.com")


#  7. browser.close()
# Runs after the test finishes
# Cleans up resources