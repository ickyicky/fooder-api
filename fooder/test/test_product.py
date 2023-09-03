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


@pytest.mark.dependency(depends=["test_list_product"])
def test_products_list_by_latest_usage(
    client, product_payload_factory, entry_payload_factory
):
    today = datetime.date.today().isoformat()
    response = client.get("diary", params={"date": today})
    assert response.status_code == 200, response.json()

    meal_id = response.json()["meals"][0]["id"]

    response = client.get("product")
    product_id = response.json()["products"][0]["id"]

    entry_payload = entry_payload_factory(meal_id, product_id, 100.0)
    response = client.post("entry", json=entry_payload)

    for _ in range(5):
        client.post("product", json=product_payload_factory()).json()["id"]

    response = client.get("product")
    assert response.json()["products"][0]["id"] == product_id
