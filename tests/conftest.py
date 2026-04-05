import pytest
from helpers.api_client import AvitoApiClient, extract_id
from helpers.data_generator import valid_item, seller_id


@pytest.fixture(scope="session")
def client():
    return AvitoApiClient()


@pytest.fixture
def created_item(client):
    payload = valid_item()
    response = client.create_item(payload)
    assert response.status_code == 200, f"Не удалось создать объявление: {response.text}"
    item_id = extract_id(response)
    return {"id": item_id, "payload": payload}


@pytest.fixture
def unique_seller_id():
    return seller_id()
