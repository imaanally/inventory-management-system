
from unittest.mock import patch, Mock
import requests

import cli


@patch("cli.requests.get")
def test_view_inventory(mock_get, capsys):
    mock_get.return_value = Mock(
        status_code=200,
        json=lambda: [
            {
                "id": 1,
                "name": "Almond Milk",
                "quantity": 20,
                "price": 450.0,
            }
        ],
    )

    cli.view_inventory()

    output = capsys.readouterr().out
    assert "Almond Milk" in output
    assert "Quantity: 20" in output
    mock_get.assert_called_once()


@patch("cli.requests.post")
@patch("builtins.input", side_effect=[
    "Mango Juice",
    "Del Monte",
    "1234567890123",
    "Beverages",
    "10",
    "150",
])
def test_add_inventory_item(mock_input, mock_post, capsys):
    mock_post.return_value = Mock(
        status_code=201,
        json=lambda: {"id": 3, "name": "Mango Juice"},
    )

    cli.add_inventory_item()

    output = capsys.readouterr().out
    assert "Item added successfully" in output
    assert mock_post.call_args.kwargs["json"]["name"] == "Mango Juice"
    assert mock_post.call_args.kwargs["json"]["quantity"] == 10


@patch("cli.requests.patch")
@patch("builtins.input", side_effect=["3", "1", "175"])
def test_update_inventory_price(mock_input, mock_patch, capsys):
    mock_patch.return_value = Mock(
        status_code=200,
        json=lambda: {"id": 3, "price": 175.0},
    )

    cli.update_inventory_item()

    output = capsys.readouterr().out
    assert "Item updated successfully" in output
    assert mock_patch.call_args.kwargs["json"] == {"price": 175.0}


@patch("cli.requests.delete")
@patch("builtins.input", return_value="3")
def test_delete_inventory_item(mock_input, mock_delete, capsys):
    mock_delete.return_value = Mock(status_code=200)

    cli.delete_inventory_item()

    output = capsys.readouterr().out
    assert "Item deleted successfully" in output
    mock_delete.assert_called_once()


@patch("cli.requests.get")
@patch("builtins.input", side_effect=["1", "1234567890123", "n"])
def test_find_product_by_barcode(mock_input, mock_get, capsys):
    mock_get.return_value = Mock(
        status_code=200,
        json=lambda: {
            "barcode": "1234567890123",
            "name": "Mango Juice",
            "brand": "Del Monte",
            "category": "Beverages",
        },
    )

    cli.find_product()

    output = capsys.readouterr().out
    assert "Mango Juice" in output
    assert "Product not added" in output
    mock_get.assert_called_once()
