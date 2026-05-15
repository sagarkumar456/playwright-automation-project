import pytest
from pytest_bdd import given

from pageObjects.login import LoginPage
from utills.apiBaseFramework import APIUtils
@pytest.fixture
def shared_data():
    return {}


@given('user has placed an order using {username} and {password}')
def place_item_order(playwright,username,password):
    user_credentials={}
    user_credentials['username'] = username
    user_credentials['password'] = password
    API_utils = APIUtils()
    orderId = API_utils.createOrder(playwright, user_credentials)


@given('user is on landing pag')
def user_is_on_landing_pag(browserInstance):
    loginPage = LoginPage(browserInstance)  # Object for Login Class
    loginPage.navigate()



@when('user logs into portal with {username} and {password}')
def user_logs_into_portal(username,password):
    dashBoradpage =loginPage.login(userName, password)


