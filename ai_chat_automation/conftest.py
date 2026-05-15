import pytest
from playwright.sync_api import sync_playwright


@pytest.fixture(scope="function")
def page():
    with sync_playwright() as p:
        # Browser launch settings
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(no_viewport=False)
        page = context.new_page()

        yield page

        # Cleanup after test
        page.close()
        context.close()
        browser.close()