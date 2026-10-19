
import pytest

from app import app
from inventory import inventory


@pytest.fixture
def client():
    original_inventory = [item.copy() for item in inventory]

    app.config["TESTING"] = True

    with app.test_client() as test_client:
        yield test_client

    inventory.clear()
    inventory.extend(original_inventory)


def test_get_all_inventory(client):
    response = client.get("/inventory")

    assert response.status_code == 200
    assert len(response.get_json()) == 2


def test_get_existing_item(client):
    response = client.get("/inventory/1")

    assert response.status_code == 200
    assert response.get_json()["name"] == "Organic Almond Milk"


def test_get_missing_item(client):
    response = client.get("/inventory/999")

    assert response.status_code == 404
    assert response.get_json()["error"] == "Inventory item not found."


def test_create_item(client):
    response = client.post(
        "/inventory",
        json={
            "name": "Green Tea",
            "quantity": 10,
            "price": 250.00,
        },
    )

    assert response.status_code == 201
    assert response.get_json()["name"] == "Green Tea"
    assert response.get_json()["id"] == 3


def test_patch_item(client):
    response = client.patch(
        "/inventory/1",
        json={"price": 475.00},
    )

    assert response.status_code == 200
    assert response.get_json()["price"] == 475.00
    assert response.get_json()["quantity"] == 20


def test_delete_item(client):
    response = client.delete("/inventory/2")

    assert response.status_code == 200
    assert response.get_json()["item"]["id"] == 2

    missing_response = client.get("/inventory/2")
    assert missing_response.status_code == 404


def test_reject_invalid_item(client):
    response = client.post(
        "/inventory",
        json={
            "name": "Green Tea",
            "quantity": -5,
            "price": 250.00,
        },
    )

    assert response.status_code == 400
    assert "error" in response.get_json()
