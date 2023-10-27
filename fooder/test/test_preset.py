import datetime
import pytest


@pytest.mark.dependency()
def test_create_meal(
    client, meal_payload_factory, product_payload_factory, entry_payload_factory
):
    today = datetime.date.today().isoformat()
    response = client.get("diary", params={"date": today})

    diary_id = response.json()["id"]
    meal_order = len(response.json()["meals"]) + 1

    response = client.post("meal", json=meal_payload_factory(diary_id, meal_order))
    assert response.status_code == 200, response.json()

    meal_id = response.json()["id"]

    product_id = client.post("product", json=product_payload_factory()).json()["id"]

    entry_payload = entry_payload_factory(meal_id, product_id, 100.0)
    response = client.post("entry", json=entry_payload)
    assert response.status_code == 200, response.json()


@pytest.mark.dependency(depends=["test_create_meal"])
def test_save_meal(client, meal_save_payload):
    today = datetime.date.today().isoformat()
    response = client.get("diary", params={"date": today})

    meal = response.json()["meals"][0]
    meal_id = meal["id"]
    save_payload = meal_save_payload(meal_id)

    response = client.post(f"meal/{meal_id}/save", json=save_payload)
    assert response.status_code == 200, response.json()

    preset = response.json()

    for k, v in preset.items():
        if k in ("id", "name", "entries"):
            continue

        assert meal[k] == v, f"{k} != {v}"


@pytest.mark.dependency(depends=["test_create_meal"])
def test_list_presets(client, meal_save_payload):
    response = client.get("preset")
    assert response.status_code == 200, response.json()
    assert len(response.json()["presets"]) > 0, response.json()

    name = meal_save_payload(0)["name"]
    response = client.get(f"preset?q={name}")
    assert response.status_code == 200, response.json()
    assert len(response.json()["presets"]) > 0, response.json()


@pytest.mark.dependency(depends=["test_list_presets"])
def test_create_meal_from_preset(client, meal_from_preset):
    today = datetime.date.today().isoformat()
    response = client.get("diary", params={"date": today})

    diary_id = response.json()["id"]
    meal_order = len(response.json()["meals"]) + 1

    response = client.get("preset")
    assert response.status_code == 200, response.json()
    assert len(response.json()["presets"]) > 0, response.json()

    preset = response.json()["presets"][0]

    payload = meal_from_preset(
        meal_order,
        diary_id,
        preset["id"],
    )

    response = client.post("meal/from_preset", json=payload)
    assert response.status_code == 200, response.json()
    meal = response.json()

    for k, v in preset.items():
        if k in ("id", "name", "entries"):
            continue

        assert meal[k] == v, f"{k} != {v}"
