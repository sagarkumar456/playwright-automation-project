from .orderHistory import OrderHistoryPage


class DashBoradpage:
    def __init__(self,page):
        self.page = page



    def selectOrdersNaviLink(self):
       self.page.get_by_role("button", name="ORDERS").click()
       orderHistoryPage= OrderHistoryPage(self.page)
       return orderHistoryPage