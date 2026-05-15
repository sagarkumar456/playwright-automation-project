import pytest
from pytest_bdd import given, when, then, parsers, scenarios

from pageObjects.login import LoginPage
from utills.apiBaseFramework import APIUtils

scenarios("../features/orderTransaction.feature")


@pytest.fixture
def share_data():
    return {}


@given(parsers.parse('user has placed an order using {username} and {password}'))
def place_item_order(playwright, username, password, share_data):
    user_credentials = {
        "userEmail": username,
        "userPassword": password
    }

    api_utils = APIUtils()
    orderId = api_utils.createOrder(playwright, user_credentials)

    share_data['orderId'] = orderId


@when('the user is on landing page')
def user_is_on_landing_page(browserInstance, share_data):
    loginPage = LoginPage(browserInstance)
    loginPage.navigate()
    share_data['login_page'] = loginPage


@when(parsers.parse('I login to portal with {username} and {password}'))
def login_page_login(username, password, share_data):
    loginPage = share_data['login_page']
    dashboard_page = loginPage.login(username, password)
    share_data['dashboard_page'] = dashboard_page


@when('navigate to orders page')
def navigate_to_orders_page(share_data):
    dashboard_page = share_data['dashboard_page']
    order_history_page = dashboard_page.selectOrdersNaviLink()
    share_data['orderHistoryPage'] = order_history_page


@when('select the orderId')
def select_orderId(share_data):
    order_history_page = share_data['orderHistoryPage']
    orderId = share_data['orderId']
    order_details_page = order_history_page.selectOrder(orderId)
    share_data['orderDetailsPage'] = order_details_page


@then('order message is successfully displayed')
def order_message(share_data):
    order_details_page = share_data['orderDetailsPage']
    order_details_page.verifyOrderMessage()