from Onelap_webstie_project.Vidsure1_code.pages.product_list_page import ProductListPage
from Onelap_webstie_project.Vidsure1_code.pages.product_detail_page import ProductDetailPage
from Onelap_webstie_project.Vidsure1_code.pages.cart_page import CartPage

def test_e2e_flow(page):

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
        cart.complete_payment("6299134504")



#Open Website → Product List Page → Click Dashcam → Product Detail Page → Select Hardware Kit → Add to Cart → Go to Cart → Click Place Order