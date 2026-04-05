from helpers.api_client import extract_id
from helpers.data_generator import valid_item


class TestStatistic:
    def test_get_statistic_matches_created_values(self, client):
        payload = valid_item()
        payload["statistics"] = {"likes": 10, "viewCount": 50, "contacts": 5}

        create_resp = client.create_item(payload)
        assert create_resp.status_code == 200
        item_id = extract_id(create_resp)

        response = client.get_statistic(item_id)
        assert response.status_code == 200

        stat = response.json()[0]
        assert stat["likes"] == 10
        assert stat["viewCount"] == 50
        assert stat["contacts"] == 5

    def test_get_statistic_response_structure(self, client, created_item):
        response = client.get_statistic(created_item["id"])
        assert response.status_code == 200

        stats = response.json()
        assert isinstance(stats, list) and len(stats) > 0

        stat = stats[0]
        assert isinstance(stat["likes"], int)
        assert isinstance(stat["viewCount"], int)
        assert isinstance(stat["contacts"], int)

    # TC-028 — баг: нулевые значения статистики не принимаются, хотя должны
    def test_get_statistic_with_zero_values(self, client):
        payload = valid_item()
        payload["statistics"] = {"likes": 0, "viewCount": 0, "contacts": 0}

        create_resp = client.create_item(payload)
        assert create_resp.status_code == 200, (
            f"ожидали 200 при создании с нулевой статистикой, получили {create_resp.status_code}"
        )

        stat_resp = client.get_statistic(extract_id(create_resp))
        assert stat_resp.status_code == 200
        stat = stat_resp.json()[0]
        assert stat["likes"] == 0
        assert stat["viewCount"] == 0
        assert stat["contacts"] == 0

    def test_get_statistic_nonexistent_id(self, client):
        response = client.get_statistic("00000000-0000-0000-0000-000000000000")
        assert response.status_code == 404

    def test_get_statistic_invalid_id_format(self, client):
        response = client.get_statistic("not-a-uuid")
        assert response.status_code in (400, 404)
