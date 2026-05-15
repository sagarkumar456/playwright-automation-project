import json
import os
import pytest

from pytest_bdd import scenarios, given, when, then

from Onelap_webstie_project.Vidsure1_code.pages.product_list_page import ProductListPage
from Onelap_webstie_project.Vidsure1_code.pages.product_detail_page import ProductDetailPage
from Onelap_webstie_project.Vidsure1_code.pages.cart_page import CartPage
from Onelap_webstie_project.Vidsure1_code.pages.razorpay_Contact_details import PaymentPage
from Onelap_webstie_project.Vidsure1_code.pages.payment_address_page import AddressPage
from Onelap_webstie_project.Vidsure1_code.pages.KotakBankPage import KotakBankPage
from Onelap_webstie_project.Vidsure1_code.utills.api_utils import ApiUtils


# -----------------------------------
# Connect Feature File
# -----------------------------------
scenarios("features/test_e2e_flow.feature")


# -----------------------------------
# Test Data Fixture
# -----------------------------------
@pytest.fixture
def test_data():

    file_path = os.path.join(
        os.path.dirname(__file__),
        "data",
        "address_data.json"
    )

    with open(file_path) as f:
        data = json.load(f)

    return data


# -----------------------------------
# Shared Data Fixture
# -----------------------------------
@pytest.fixture
def shared_data( ):
    return {}


# -----------------------------------
# Step Definitions
# -----------------------------------

@given("User opens the product listing page")
def open_product_page(page):

    product_list = ProductListPage(page)
    product_list.goto()


@when("User selects a product from the list")
def select_product(page):

    product_list = ProductListPage(page)
    product_list.click_first_product()


@when("User selects hardwiring kit and adds product to cart")
def add_product_to_cart(page):

    product_detail = ProductDetailPage(page)

    product_detail.select_hardwiring_kit()
    product_detail.add_product_to_cart()
    product_detail.go_to_cart()


@when("User proceeds to cart and places the order")
def place_order(page):

    cart = CartPage(page)
    cart.place_order()


@when("User enters contact details with phone number")
def enter_contact_details(page, test_data):

    payment = PaymentPage(page)

    payment.razorpay_Contact_details(
        test_data["phone"]
    )


@when("User fills the address details")
def fill_address(page, test_data):

    address = AddressPage(page)

    address.fill_address_details(
        **test_data["address"]
    )

    address.click_continue()


@when("User selects Netbanking payment option")
def select_netbanking(page, shared_data):

    kotak = KotakBankPage(page)

    kotak.select_kotak_bank()

    shared_data["kotak"] = kotak


@then("System should capture payment ID")
def capture_payment_id(page, shared_data):

    api_utils = ApiUtils(page)

    kotak = shared_data["kotak"]

    payment_id = api_utils.capture_payment_from_ui(
        kotak.click_success
    )

    print(f"\nPayment ID captured: {payment_id}")

    shared_data["payment_id"] = payment_id


@then("Order should be verified in Control system")
def verify_order(page, shared_data, test_data):

    api_utils = ApiUtils(page)

    control_data = api_utils.check_order_in_Control(
        payment_id=shared_data["payment_id"],
        phone_number=test_data["phone"]
    )

    print(f"Control Response: {control_data}")

    assert control_data is not None

    print("Order Verified Successfully")