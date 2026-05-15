# api_automation_project/conftest.py
import pytest
from playwright.sync_api import sync_playwright

@pytest.fixture(scope="session")
def api_context():
    with sync_playwright() as p:
        # ignore_https_errors=True add karne se expired certificate wala error nahi aayega
        request_context = p.request.new_context(ignore_https_errors=True)
        yield request_context
        request_context.dispose()