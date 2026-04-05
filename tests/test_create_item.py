from helpers.api_client import extract_id
from helpers.data_generator import valid_item


class TestCreateItem:
    def test_create_with_valid_data(self, client):
        # смотрим, а создание вообще работает?
        payload = valid_item()
        response = client.create_item(payload)
        assert response.status_code == 200
        item_id = extract_id(response)
        assert item_id, "id не должен быть пустым"

    def test_created_items_have_unique_ids(self, client):
        payload = valid_item()
        r1 = client.create_item(payload)
        r2 = client.create_item(payload)
        assert r1.status_code == 200
        assert r2.status_code == 200
        assert extract_id(r1) != extract_id(r2), "два объявления с одинаковыми данными должны получать разные id"

    def test_create_with_zero_price(self, client):
        # нулевая цена — краевой случай, не очевидно как должен вести себя сервис
        payload = valid_item()
        payload["price"] = 0
        response = client.create_item(payload)
        assert response.status_code in (200, 400)

    # TC-004 — баг
    def test_create_with_negative_price(self, client):
        payload = valid_item()
        payload["price"] = -100
        response = client.create_item(payload)
        assert response.status_code == 400, (
            f"ожидали 400, получили {response.status_code} — "
            "API не должен принимать отрицательную цену"
        )

    def test_create_without_name(self, client):
        payload = valid_item()
        del payload["name"]
        resp = client.create_item(payload)
        assert resp.status_code == 400

    def test_create_without_price(self, client):
        payload = valid_item()
        del payload["price"]
        resp = client.create_item(payload)
        assert resp.status_code == 400

    def test_create_without_seller_id(self, client):
        payload = valid_item()
        del payload["sellerId"]
        resp = client.create_item(payload)
        assert resp.status_code == 400

    def test_create_with_empty_body(self, client):
        response = client.create_item({})
        assert response.status_code == 400

    def test_create_with_string_price(self, client):
        payload = valid_item()
        payload["price"] = "дорого"
        response = client.create_item(payload)
        assert response.status_code == 400

    def test_create_with_string_seller_id(self, client):
        payload = valid_item()
        payload["sellerId"] = "abc"
        response = client.create_item(payload)
        assert response.status_code == 400

    def test_create_with_very_long_name(self, client):
        payload = valid_item()
        payload["name"] = "а" * 1000
        response = client.create_item(payload)
        # Не знаем есть ли ограничение на длину
        assert response.status_code in (200, 400)

    # TC-012 — баг
    def test_create_with_negative_statistics(self, client):
        payload = valid_item()
        payload["statistics"] = {"likes": -1, "viewCount": -5, "contacts": -10}
        response = client.create_item(payload)
        assert response.status_code == 400, (
            f"ожидали 400, получили {response.status_code} — "
            "отрицательные значения статистики не должны приниматься"
        )

    def test_create_same_data_returns_different_ids(self, client):
        # Проверка идемпотентности
        payload = valid_item()
        r1 = client.create_item(payload)
        r2 = client.create_item(payload)
        assert r1.status_code == 200
        assert r2.status_code == 200
        assert extract_id(r1) != extract_id(r2)

    def test_create_with_special_chars_in_name(self, client):
        payload = valid_item()
        payload["name"] = "<script>alert(1)</script>"
        response = client.create_item(payload)
        assert response.status_code in (200, 400)
