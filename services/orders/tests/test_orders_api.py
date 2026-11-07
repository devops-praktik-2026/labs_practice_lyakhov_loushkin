def test_create_order_returns_201(client, order_payload):
    response = client.post("/orders", json=order_payload)
    assert response.status_code == 201
    data = response.json()
    assert data["item"] == order_payload["item"]
    assert data["quantity"] == order_payload["quantity"]

def test_invalid_payload_returns_422(client):
    invalid_payload = {"account_id": 1, "item": "Тест", "quantity": 0}
    response = client.post("/orders", json=invalid_payload)
    assert response.status_code == 422

def test_get_order_by_id_returns_200(client, order_payload):
    create_res = client.post("/orders", json=order_payload)
    order_id = create_res.json()["id"]
    
    response = client.get(f"/orders/{order_id}")
    assert response.status_code == 200
    assert response.json()["id"] == order_id

def test_get_order_by_id_returns_404(client):
    response = client.get("/orders/99999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Заказ 99999 не найден"

def test_get_orders_by_account_id(client, order_payload):
    client.post("/orders", json=order_payload)
    
    response = client.get("/orders?account_id=1")
    assert response.status_code == 200
    assert len(response.json()) >= 1
    
    response_empty = client.get("/orders?account_id=999")
    assert response_empty.status_code == 200
    assert response_empty.json() == []