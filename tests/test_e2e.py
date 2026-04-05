from helpers.api_client import extract_id
from helpers.data_generator import valid_item, seller_id


class TestE2E:
    def test_create_then_get_by_id(self, client):
        # Создаём объявление и сразу проверяем что оно получается по id
        payload = valid_item()
        create_resp = client.create_item(payload)
        assert create_resp.status_code == 200
        item_id = extract_id(create_resp)

        get_resp = client.get_item(item_id)
        assert get_resp.status_code == 200

        item = get_resp.json()[0]
        assert item["id"] == item_id
        assert item["name"] == payload["name"]
        assert item["price"] == payload["price"]
        assert item["sellerId"] == payload["sellerId"]

    def test_create_multiple_then_get_by_seller(self, client):
        sid = seller_id()
        created_ids = []

        for _ in range(3):
            r = client.create_item(valid_item(seller=sid))
            assert r.status_code == 200
            created_ids.append(extract_id(r))

        list_resp = client.get_seller_items(sid)
        assert list_resp.status_code == 200

        returned_ids = [item["id"] for item in list_resp.json()]
        for item_id in created_ids:
            assert (
                item_id in returned_ids
            ), f"объявление {item_id} не нашлось в выдаче продавца"

    def test_create_then_check_statistic(self, client):
        # Проверяем что статистика совпадает с тем, что отдаёт ручка статистики
        payload = valid_item()
        payload["statistics"] = {"likes": 7, "viewCount": 42, "contacts": 3}

        create_resp = client.create_item(payload)
        assert create_resp.status_code == 200
        item_id = extract_id(create_resp)

        stat_resp = client.get_statistic(item_id)
        assert stat_resp.status_code == 200

        stat = stat_resp.json()[0]
        assert stat["likes"] == payload["statistics"]["likes"]
        assert stat["viewCount"] == payload["statistics"]["viewCount"]
        assert stat["contacts"] == payload["statistics"]["contacts"]
