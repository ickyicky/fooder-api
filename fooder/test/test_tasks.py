import pytest


@pytest.mark.anyio
async def test_cache_product_usage(client, tasks_client):
    response = await client.get("product")
    assert response.status_code == 200, response.json()
    old_data = response.json()

    response = await tasks_client.post("/cache_product_usage_data")
    assert response.status_code == 200, response.json()

    response = await client.get("product")
    assert response.status_code == 200, response.json()
    assert response.json() != old_data
