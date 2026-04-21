import json
import time

import pytest
from playwright.sync_api import Playwright, expect

from pageObjects.login import LoginPage
from pageObjects.dashborad import DashBoradpage
from utills.apiBaseFramework import APIUtils

#from utills.apiBaseFramework import APIUtils

# json → JSON file read karne ke lye
# pytest → test runner + parametrize
# Playwright → API & browser control
# expect → assertions (PASS/FAIL)
# APIUtils → reusable API logic

#json file -> util -> access into test
with open('/ai_chat_automation/data/messages.json') as f:
    test_data = json.load(f)
    print(test_data)
    user_credential_List = test_data['user_credential']

@pytest.mark.parametrize('user_credentials', user_credential_List)


@pytest.mark.smoke
def test_e2n_web_api(playwright: Playwright,browserInstance, user_credentials):

    userName= user_credentials['userEmail']
    password = user_credentials['userPassword']

    #create order->createId
    API_utils=APIUtils()
    orderId =API_utils.createOrder(playwright,user_credentials)

    #login
    loginPage =LoginPage(browserInstance) #Object for Login Class
    loginPage.navigate()
    dashBoradpage =loginPage.login(userName, password)

    #dashBord_page

    OrderHistoryPage = dashBoradpage.selectOrdersNaviLink()
    orderDetailsPage = OrderHistoryPage.selectOrder(orderId)
    orderDetailsPage.verifyOrderMessage()









