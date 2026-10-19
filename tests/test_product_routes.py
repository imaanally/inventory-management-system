
from unittest.mock import patch

import requests

from app import app


def test_barcode_route_success():
    with patch(
        "app.find_product_by_barcode",
        return_value={
            "barcode": "123",
            "name": "Green Tea",
            "brand": "Tea Company",
            "ingredients": "Green tea",
            "category": "Beverages",
        },
    ):
        response = app.test_client().get("/products/barcode/123")

    assert response.status_code == 200
    assert response.get_json()["name"] == "Green Tea"


def test_barcode_route_product_not_found():
    with patch("app.find_product_by_barcode", return_value=None):
        response = app.test_client().get("/products/barcode/000")

    assert response.status_code == 404


def test_barcode_route_api_failure():
    with patch(
        "app.find_product_by_barcode",
        side_effect=requests.ConnectionError,
    ):
        response = app.test_client().get("/products/barcode/123")

    assert response.status_code == 502


def test_name_search_route_success():
    with patch(
        "app.search_products_by_name",
        return_value=[{"name": "Green Tea", "barcode": "123"}],
    ):
        response = app.test_client().get(
            "/products/search?name=Green%20Tea"
        )

    assert response.status_code == 200
    assert response.get_json()["products"][0]["name"] == "Green Tea"


def test_name_search_route_requires_name():
    response = app.test_client().get("/products/search")

    assert response.status_code == 400
