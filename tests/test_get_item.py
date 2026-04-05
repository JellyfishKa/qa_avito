class TestGetItem:
    def test_get_existing_item(self, client, created_item):
        response = client.get_item(created_item["id"])
        assert response.status_code == 200

        # Ответ приходит списком, берём первый элемент
        items = response.json()
        assert isinstance(items, list) and len(items) == 1

        item = items[0]
        assert item["id"] == created_item["id"]
        assert item["name"] == created_item["payload"]["name"]
        assert item["price"] == created_item["payload"]["price"]
        assert item["sellerId"] == created_item["payload"]["sellerId"]

    def test_get_item_response_field_types(self, client, created_item):
        resp = client.get_item(created_item["id"])
        assert resp.status_code == 200
        item = resp.json()[0]

        assert isinstance(item["id"], str)
        assert isinstance(item["sellerId"], int)
        assert isinstance(item["name"], str)
        assert isinstance(item["price"], int)
        assert isinstance(item["statistics"], dict)
        assert isinstance(item["createdAt"], str)

    def test_get_nonexistent_item(self, client):
        resp = client.get_item("00000000-0000-0000-0000-000000000000")
        assert resp.status_code == 404

    def test_get_item_invalid_id_format(self, client):
        response = client.get_item("abc123")
        assert response.status_code in (400, 404)

    def test_get_item_empty_id(self, client):
        # Проверяем что сервер не падает на пустом id
        response = client.get_item("")
        assert response.status_code in (400, 404)
