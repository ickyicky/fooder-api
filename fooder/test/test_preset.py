import datetime
import pytest


@pytest.mark.anyio
async def test_create_meal(
    client, meal_payload_factory, product_payload_factory, entry_payload_factory
):
    today = datetime.date.today().isoformat()
    response = await client.get("diary", params={"date": today})

    diary_id = response.json()["id"]
    meal_order = len(response.json()["meals"]) + 1

    response = await client.post(
        "meal", json=meal_payload_factory(diary_id, meal_order)
    )
    assert response.status_code == 200, response.json()

    meal_id = response.json()["id"]

    product_id = (await client.post("product", json=product_payload_factory())).json()[
        "id"
    ]

    entry_payload = entry_payload_factory(meal_id, product_id, 100.0)
    response = await client.post("entry", json=entry_payload)
    assert response.status_code == 200, response.json()


@pytest.mark.anyio
async def test_save_meal(client, meal_save_payload):
    today = datetime.date.today().isoformat()
    response = await client.get("diary", params={"date": today})

    meal = response.json()["meals"][0]
    meal_id = meal["id"]
    save_payload = meal_save_payload(meal_id)

    response = await client.post(f"meal/{meal_id}/save", json=save_payload)
    assert response.status_code == 200, response.json()

    preset = response.json()

    for k, v in preset.items():
        if k in ("id", "name", "entries"):
            continue

        assert meal[k] == v, f"{k} != {v}"


@pytest.mark.anyio
async def test_list_presets(client, meal_save_payload):
    response = await client.get("preset")
    assert response.status_code == 200, response.json()
    assert len(response.json()["presets"]) > 0, response.json()

    name = meal_save_payload(0)["name"]
    response = await client.get(f"preset?q={name}")
    assert response.status_code == 200, response.json()
    assert len(response.json()["presets"]) > 0, response.json()


@pytest.mark.anyio
async def test_create_meal_from_preset(client, meal_from_preset):
    today = datetime.date.today().isoformat()
    response = await client.get("diary", params={"date": today})

    diary_id = response.json()["id"]
    meal_order = len(response.json()["meals"]) + 1

    response = await client.get("preset")
    assert response.status_code == 200, response.json()
    assert len(response.json()["presets"]) > 0, response.json()

    preset = response.json()["presets"][0]

    payload = meal_from_preset(
        meal_order,
        diary_id,
        preset["id"],
    )

    response = await client.post("meal/from_preset", json=payload)
    assert response.status_code == 200, response.json()
    meal = response.json()

    for k, v in preset.items():
        if k in ("id", "name", "entries"):
            continue

        assert meal[k] == v, f"{k} != {v}"


@pytest.mark.anyio
async def test_delete_preset(client):
    presets = (await client.get("preset")).json()["presets"]
    preset_id = presets[0]["id"]

    response = await client.get(f"preset/{preset_id}")
    assert response.status_code == 200, response.json()

    response = await client.delete(f"preset/{preset_id}")
    assert response.status_code == 200, response.json()

    response = await client.get(f"preset/{preset_id}")
    assert response.status_code == 404, response.json()
