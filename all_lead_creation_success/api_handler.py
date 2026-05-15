class ApiInterceptor:
    def __init__(self):
        self.results = {
            "TALK_TO_EXPERT": False,
            "Stand A Chance": False,
            "CONTACT_FORM": False
        }

    def handle_response(self, response):
        # Hum check kar rahe hain ki kya ye hamari specific contact API hai
        if "sendContactForm" in response.url:
            try:
                # Request data nikalne ke liye (taaki pata chale kaunsa element submit hua)
                request_payload = response.request.post_data_json
                element = request_payload.get("element")
                title = request_payload.get("title")

                if response.status == 200:
                    print(f"Success: {element if element else title} Lead Created")

                    # Jis type ki lead hai usko True mark karein
                    if element == "TALK_TO_EXPERT":
                        self.results["TALK_TO_EXPERT"] = True
                    elif element == "CONTACT_FORM":
                        self.results["CONTACT_FORM"] = True
                    elif title == "Stand A Chance":
                        self.results["Stand A Chance"] = True
                else:
                    print(f"Failed: API returned status {response.status} for {element}")
            except Exception as e:
                print(f"Error parsing API: {e}")

    def check_success(self, lead_key):
        return self.results.get(lead_key, False)