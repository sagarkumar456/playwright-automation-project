#test case
#step 1 : open www.onelap.in
#step 2 Click on Product Listing Card (GO-plus)
#step 3 : Product Card → Product Detail Page → Add to Cart → Open Cart → Apply Coupon → Checkout → Payment → Order Success.
import time

from playwright.sync_api import Page


def test_OnelapProduct_Listing(page: Page):
    page.goto("https://www.onelap.in/")
    page.get_by_role("img",name="Onelap GO plu").click()
    page.get_by_role("button",name="Add to cart").click()
    page.get_by_role("button", name="shopping_cart Go to Cart").click()
    # page.get_by_text("add_circle_outline").click()
    # page.get_by_role("button", name="Apply").click()
    # page.locator("#mat-checkbox-2 > .mat-checkbox-layout > .mat-checkbox-inner-container").click()
    # page.locator("#notMin2002").get_by_role("button", name="Apply").click()
    # page.get_by_role("button", name="PLACE ORDER").click()

    time.sleep(5)
