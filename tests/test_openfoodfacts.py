
from unittest.mock import Mock, patch

import pytest
import requests

from openfoodfacts import (
    find_product_by_barcode,
    search_products_by_name,
)


@patch("openfoodfacts.requests.get")
def test_find_product_by_barcode(mock_get):
    mock_response = Mock()
    mock_response.json.return_value = {
        "status": 1,
        "product": {
            "code": "0123456789012",
            "product_name": "Organic Almond Milk",
            "brands": "Silk",
            "ingredients_text": "Water, almonds",
            "categories": "Beverages",
        },
    }
    mock_get.return_value = mock_response

    product = find_product_by_barcode("0123456789012")

    assert product["name"] == "Organic Almond Milk"
    assert product["brand"] == "Silk"
    assert product["barcode"] == "0123456789012"
    mock_get.assert_called_once()


@patch("openfoodfacts.requests.get")
def test_barcode_product_not_found(mock_get):
    mock_response = Mock()
    mock_response.json.return_value = {
        "status": 0,
        "product": None,
    }
    mock_get.return_value = mock_response

    assert find_product_by_barcode("0000000000000") is None


@patch("openfoodfacts.requests.get")
def test_search_products_by_name(mock_get):
    mock_response = Mock()
    mock_response.json.return_value = {
        "products": [
            {
                "code": "123",
                "product_name": "Green Tea",
                "brands": "Tea Company",
                "ingredients_text": "Green tea",
                "categories": "Beverages",
            },
            {
                "code": "456",
                "product_name": "Green Tea with Mint",
                "brands": "Minty",
                "ingredients_text": "Green tea, mint",
                "categories": "Beverages",
            },
        ]
    }
    mock_get.return_value = mock_response

    products = search_products_by_name("Green Tea")

    assert len(products) == 2
    assert products[0]["name"] == "Green Tea"
    assert products[1]["name"] == "Green Tea with Mint"


def test_reject_empty_barcode():
    with pytest.raises(ValueError):
        find_product_by_barcode(" ")


def test_reject_empty_product_name():
    with pytest.raises(ValueError):
        search_products_by_name(" ")


@patch("openfoodfacts.requests.get")
def test_barcode_api_failure(mock_get):
    mock_response = Mock()
    mock_response.raise_for_status.side_effect = requests.HTTPError(
        "Service unavailable"
    )
    mock_get.return_value = mock_response

    with pytest.raises(requests.HTTPError):
        find_product_by_barcode("0123456789012")
