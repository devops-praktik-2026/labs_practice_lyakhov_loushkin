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

def test_get_order_by_id_returns_200(client, order_payload):
    # Сначала создаём заказ
    create_response = client.post("/orders", json=order_payload)
    order_id = create_response.json()["id"]

    # Получаем его по ID
    response = client.get(f"/orders/{order_id}")
    
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == order_id
    assert data["item"] == order_payload["item"]
    assert data["quantity"] == order_payload["quantity"]


def test_get_order_by_id_returns_404(client):
    # Запрашиваем несуществующий заказ
    response = client.get("/orders/99999")
    
    assert response.status_code == 404
    assert response.json()["detail"] == "Заказ 99999 не найден"