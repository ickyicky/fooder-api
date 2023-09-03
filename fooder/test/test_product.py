import pytest
import datetime


@pytest.mark.dependency()
def test_create_product(client, product_payload):
    response = client.post("product", json=product_payload)
    assert response.status_code == 200, response.json()


@pytest.mark.dependency(depends=["test_create_product"])
def test_list_product(client):
    response = client.get("product")
    assert response.status_code == 200, response.json()

    data = response.json()["products"]
    assert len(data) != 0

    product_ids = set()
    for product in data:
        assert product["id"] not in product_ids
        product_ids.add(product["id"])
