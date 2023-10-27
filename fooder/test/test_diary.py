import datetime
import pytest


@pytest.mark.dependency()
def test_get_diary(client):
    today = datetime.date.today().isoformat()
    response = client.get("diary", params={"date": today})
    assert response.status_code == 200, response.json()

    assert response.json()["date"] == today
    # new diary should contain exactly one meal
    assert len(response.json()["meals"]) == 1


@pytest.mark.dependency(depends=["test_get_diary"])
def test_diary_add_meal(client, meal_payload_factory):
    today = datetime.date.today().isoformat()
    response = client.get("diary", params={"date": today})

    diary_id = response.json()["id"]
    meal_order = len(response.json()["meals"]) + 1

    response = client.post("meal", json=meal_payload_factory(diary_id, meal_order))
    assert response.status_code == 200, response.json()


@pytest.mark.dependency(depends=["test_diary_add_meal"])
def test_diary_delete_meal(client):
    today = datetime.date.today().isoformat()
    response = client.get("diary", params={"date": today})

    meals_amount = len(response.json()["meals"])
    meal_id = response.json()["meals"][0]["id"]

    response = client.delete(f"meal/{meal_id}")
    assert response.status_code == 200, response.json()

    response = client.get("diary", params={"date": today})
    assert response.status_code == 200, response.json()
    assert len(response.json()["meals"]) == meals_amount - 1


@pytest.mark.dependency(depends=["test_get_diary"])
def test_diary_add_entry(client, product_payload_factory, entry_payload_factory):
    today = datetime.date.today().isoformat()
    response = client.get("diary", params={"date": today})

    meal_id = response.json()["meals"][0]["id"]

    product_id = client.post("product", json=product_payload_factory()).json()["id"]

    entry_payload = entry_payload_factory(meal_id, product_id, 100.0)
    response = client.post("entry", json=entry_payload)
    assert response.status_code == 200, response.json()


@pytest.mark.dependency(depends=["test_diary_add_entry"])
def test_diary_edit_entry(client, entry_payload_factory):
    today = datetime.date.today().isoformat()
    response = client.get("diary", params={"date": today})

    entry = response.json()["meals"][0]["entries"][0]
    id_ = entry["id"]
    entry_payload = entry_payload_factory(
        entry["meal_id"], entry["product"]["id"], entry["grams"] + 100.0
    )

    response = client.patch(f"entry/{id_}", json=entry_payload)
    assert response.status_code == 200, response.json()
    assert response.json()["grams"] == entry_payload["grams"]


@pytest.mark.dependency(depends=["test_diary_add_entry"])
def test_diary_delete_entry(client):
    today = datetime.date.today().isoformat()
    response = client.get("diary", params={"date": today})

    entry_id = response.json()["meals"][0]["entries"][0]["id"]
    response = client.delete(f"entry/{entry_id}")
    assert response.status_code == 200, response.json()

    response = client.get("diary", params={"date": today})
    assert response.status_code == 200, response.json()
    deleted_entries = [
        entry
        for meal in response.json()["meals"]
        for entry in meal["entries"]
        if entry["id"] == entry_id
    ]
    assert len(deleted_entries) == 0
