from playwright.sync_api import Page

class ProductListPage:

    def __init__(self, page: Page):
        self.page = page
        self.product_items = ".product-item"
        self.first_product = ".product-item >> nth=0"

    def goto(self):
        self.page.goto("https://test.onelap.in/")

    def click_first_product(self):
        self.page.get_by_text("Onelap VidSure - 3K UHD Car Dashcam").click()

    def select_product(self,product_name):
        self.page.get_by_text(product_name , exact= True).click()

