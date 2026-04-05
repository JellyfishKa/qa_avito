from helpers.data_generator import valid_item, seller_id


class TestGetSellerItems:
    def test_get_items_for_seller_with_one_item(self, client):
        sid = seller_id()
        r = client.create_item(valid_item(seller=sid))
        assert r.status_code == 200

        response = client.get_seller_items(sid)
        assert response.status_code == 200

        items = response.json()
        assert isinstance(items, list)
        assert len(items) == 1
        assert items[0]["sellerId"] == sid

    def test_get_items_for_seller_with_multiple_items(self, client):
        sid = seller_id()
        for _ in range(3):
            r = client.create_item(valid_item(seller=sid))
            assert r.status_code == 200

        response = client.get_seller_items(sid)
        assert response.status_code == 200
        assert len(response.json()) == 3

    def test_seller_items_belong_only_to_that_seller(self, client):
        sid = seller_id()
        other_sid = seller_id()

        client.create_item(valid_item(seller=sid))
        client.create_item(valid_item(seller=other_sid))

        items = client.get_seller_items(sid).json()
        for item in items:
            assert item["sellerId"] == sid

    def test_get_items_for_seller_without_items(self, client):
        # Генерируем заведомо новый sellerId без объявлений
        sid = seller_id()
        response = client.get_seller_items(sid)
        assert response.status_code in (200, 404)
        if response.status_code == 200:
            assert response.json() == []

    def test_get_items_invalid_seller_id_string(self, client):
        response = client.get_seller_items("abc")
        assert response.status_code == 400

    # TC-025 — баг
    def test_get_items_negative_seller_id(self, client):
        response = client.get_seller_items(-1)
        assert response.status_code in (400, 404), (
            f"ожидали 400/404 для sellerId=-1, получили {response.status_code}"
        )
