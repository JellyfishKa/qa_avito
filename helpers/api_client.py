import requests

BASE_URL = "https://qa-internship.avito.com"


class AvitoApiClient:
    def __init__(self, base_url=BASE_URL):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update(
            {"Content-Type": "application/json", "Accept": "application/json"}
        )

    def create_item(self, payload):
        return self.session.post(f"{self.base_url}/api/1/item", json=payload)

    def get_item(self, item_id):
        return self.session.get(f"{self.base_url}/api/1/item/{item_id}")

    def get_seller_items(self, seller_id):
        return self.session.get(f"{self.base_url}/api/1/{seller_id}/item")

    def get_statistic(self, item_id):
        return self.session.get(f"{self.base_url}/api/1/statistic/{item_id}")


def extract_id(create_response):
    status_msg = create_response.json().get("status", "")
    return status_msg.split(" - ")[-1]
