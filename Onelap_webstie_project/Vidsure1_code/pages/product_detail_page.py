from playwright.sync_api import Page


class ProductDetailPage:

    def __init__(self, page: Page):
        self.page = page

        # Locators
        self.hardwiring_kit_btn = "div:has-text('Hardwiring kit') span.custom-button"
        self.add_to_cart_btn = "text=Add to cart"
        self.go_to_cart_btn = "text=Go to Cart"

    def select_hardwiring_kit(self):
        self.page.locator(self.hardwiring_kit_btn).first.click()

    def add_product_to_cart(self):
        self.page.get_by_text("Add to cart", exact=True).click()

    def go_to_cart(self):
        self.page.get_by_text("Go to Cart", exact=True).click()