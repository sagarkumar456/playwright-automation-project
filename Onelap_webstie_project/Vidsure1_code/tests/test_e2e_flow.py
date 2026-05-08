import time
import json
import os

from Onelap_webstie_project.Vidsure1_code.pages.KotakBankPage import KotakBankPage
from Onelap_webstie_project.Vidsure1_code.pages.payment_address_page import AddressPage
from Onelap_webstie_project.Vidsure1_code.pages.razorpay_Contact_details import PaymentPage
from Onelap_webstie_project.Vidsure1_code.pages.product_list_page import ProductListPage
from Onelap_webstie_project.Vidsure1_code.pages.product_detail_page import ProductDetailPage
from Onelap_webstie_project.Vidsure1_code.pages.cart_page import CartPage
from Onelap_webstie_project.Vidsure1_code.utills.api_utils import ApiUtils


def load_test_data():
    file_path = os.path.join(os.path.dirname(__file__), "../data/address_data.json")
    with open(file_path) as f:
        return json.load(f)


def test_e2e_flow(page):
    # Load Test Data
    test_data = load_test_data()

    # Product List Page
    product_list = ProductListPage(page)
    product_list.goto()
    product_list.click_first_product()

    # Product Detail Page
    product_detail = ProductDetailPage(page)
    product_detail.select_hardwiring_kit()
    product_detail.add_product_to_cart()
    product_detail.go_to_cart()

    # Cart Page
    cart = CartPage(page)
    cart.place_order()

    # Payment Page
    payment = PaymentPage(page)
    payment.razorpay_Contact_details(test_data["phone"])

    # Address Page (Softcoded)
    address = AddressPage(page)
    address.fill_address_details(**test_data["address"])
    address.click_continue()

    # Kotak Bank Selection
    kotak = KotakBankPage(page)
    kotak.select_kotak_bank()

    # API Utils
    api_utils = ApiUtils(page)

    # Capture Payment ID from UI
    payment_id = api_utils.capture_payment_from_ui(kotak.click_success)
    print(f"\nPayment ID captured from UI: {payment_id}")

    # Verify Order in Control
    control_data = api_utils.check_order_in_Control(
        payment_id=payment_id,
        phone_number=test_data["phone"]
    )

    print(f"CRM API Response: {control_data}")
    print("Order Verified Successfully in Control")

    # Temporary wait (replace with proper assertion if possible)
    time.sleep(10)