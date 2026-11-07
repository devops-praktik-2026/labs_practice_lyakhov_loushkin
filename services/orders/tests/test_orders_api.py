def test_create_order_returns_201(client, order_payload):
    response = client.post("/orders", json=order_payload)
    assert response.status_code == 201
    data = response.json()
    assert data["item"] == order_payload["item"]
    assert data["quantity"] == order_payload["quantity"]
    assert "id" in data
    assert "created_at" in data


def test_invalid_payload_returns_422(client):
    invalid_payload = {
        "account_id": 1,
        "item": "Тестовый товар",
        "quantity": 0
    }
    response = client.post("/orders", json=invalid_payload)
    assert response.status_code == 422