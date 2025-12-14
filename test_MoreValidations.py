# Test Steps
#
# Navigate to the page where the Hide/Show example is available.
#
# Verify that the text "Hide/Show Example" is visible.
#
# Click on the Hide button.
#
# Validate that the content/section is no longer visible on the page
import time
from playwright.sync_api import Page, expect


def test_UICheck(page: Page):
    #hide/display and placeholder
    global PriceCalValue
    page.goto("https://rahulshettyacademy.com/AutomationPractice/")
    expect(page.get_by_placeholder("Hide/Show Example")).to_be_visible()
    page.get_by_role("button",name="Hide").click()
    expect(page.get_by_placeholder("Hide/Show Example")).to_be_hidden()

    #AlertBox
    page.on("dialog", lambda dialog:dialog.accept())
    page.get_by_role("button",name="Confirm").click()
    time.sleep(5)

    #MouseHover
    page.locator("#mousehover").hover()
    page.get_by_role("link",name="Top").click()

    #  #headel iframe
    # Page_frame = page.frame_locator("#cours")
    # Page_frame.get_by_role("link",name="All Access plan ").click()
    # expect(Page_frame.locator("body")).to_contain_text("Happy susbscibres")
    #

    #check the price of rice equal 37
    #identify rice colum
    #identify the rice row
    #extract the price of rice

    page.goto("https://rahulshettyacademy.com/seleniumPractise/#/offers")
    for index in range(page.locator("th").count()):
        if page.locator("th").nth(index).filter(has_text="Price").count()>  0:
            PriceCalValue = index;
            print(f"Price Column value id {PriceCalValue}")
            break
    RiceRow = page.locator("tr").filter(has_text="Rice")
    expect(RiceRow.page.locator("td").nth(PriceCalValue)).to_have_text("37")








