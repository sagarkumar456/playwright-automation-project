#Playwright import
from playwright.sync_api import Playwright
#orderPayLoad – Request Body sending on unique id
orderPayLoad={"orders":[{"country":"India","productOrderedId":"68a961459320a140fe1ca57a"}]}

#APIUtils class
class APIUtils:
#getToken() – Login API
    def getToken(self,playwright:Playwright):
        #API Context Create
        api_request_context = playwright.request.new_context(base_url="https://rahulshettyacademy.com/api/ecom/order/create-order")
        #POST request (Login)
        response=api_request_context.post("/api/ecom/auth/login",
                                 data={"userEmail":"skdas1641999@gamil.com","userPassword":"sagardas456"})
         #Assertion (PASS / FAIL)Agar status 200 / 201 → PASS sagar
         #Agar 401 / 403 / 500 → FAIL (test fail ho jayega)
        assert response.ok
        #Response read
        print(response.json())
        responseBody = response.json()
        return   responseBody["token"]

            #createOrder() – Order API
    def createOrder(self, playwright:Playwright):
        #Token lena
        token =self.getToken(playwright)
        #API Context
        api_request_context = playwright.request.new_context(base_url="https://rahulshettyacademy.com/api/ecom/order/create-order")
        #Create Order POST call
        #Important Headers:Authorization → token: Content - Type → JSONdata
        response = api_request_context.post("/api/ecom/order/create-order",
                                 data=orderPayLoad,
                                 headers={"Authorization":token,
                                          "Content-Type": "application/json",})
        #Response print
        print(response.json())
