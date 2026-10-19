
import requests
from flask import Flask, jsonify, request

from inventory import (
    add_item,
    delete_item,
    get_all_items,
    get_item_by_id,
    update_item,
)
from openfoodfacts import (
    find_product_by_barcode,
    search_products_by_name,
)

app = Flask(__name__)

# Fields employees can store or update.
ALLOWED_FIELDS = {
    "name",
    "brand",
    "barcode",
    "quantity",
    "price",
    "category",
}


def validate_item_data(data, partial=False):
    """Validate inventory input and return an error message if invalid."""
    if not isinstance(data, dict):
        return "Request body must be a JSON object."

    if not partial:
        missing = {"name", "quantity", "price"} - data.keys()
        if missing:
            return (
                f"Missing required fields: "
                f"{', '.join(sorted(missing))}"
            )

    unknown = data.keys() - ALLOWED_FIELDS
    if unknown:
        return f"Unknown fields: {', '.join(sorted(unknown))}"

    for field in ("name", "brand", "barcode", "category"):
        if field in data and (
            not isinstance(data[field], str)
            or not data[field].strip()
        ):
            return f"{field} must be a non-empty string."

    if "quantity" in data:
        quantity = data["quantity"]
        if (
            isinstance(quantity, bool)
            or not isinstance(quantity, int)
            or quantity < 0
        ):
            return "quantity must be a non-negative integer."

    if "price" in data:
        price = data["price"]
        if (
            isinstance(price, bool)
            or not isinstance(price, (int, float))
            or price < 0
        ):
            return "price must be a non-negative number."

    if partial and not data:
        return "Provide at least one field to update."

    return None


# -------------------------
# Inventory CRUD endpoints
# -------------------------

@app.get("/inventory")
def list_inventory():
    """Return all inventory items."""
    return jsonify(get_all_items()), 200


@app.get("/inventory/<int:item_id>")
def get_inventory_item(item_id):
    """Return one inventory item by ID."""
    item = get_item_by_id(item_id)

    if item is None:
        return jsonify({"error": "Inventory item not found."}), 404

    return jsonify(item), 200


@app.post("/inventory")
def create_inventory_item():
    """Create a new inventory item."""
    data = request.get_json(silent=True)
    error = validate_item_data(data)

    if error:
        return jsonify({"error": error}), 400

    item = add_item(data)
    return jsonify(item), 201


@app.patch("/inventory/<int:item_id>")
def patch_inventory_item(item_id):
    """Update selected fields on an inventory item."""
    data = request.get_json(silent=True)
    error = validate_item_data(data, partial=True)

    if error:
        return jsonify({"error": error}), 400

    item = update_item(item_id, data)

    if item is None:
        return jsonify({"error": "Inventory item not found."}), 404

    return jsonify(item), 200


@app.delete("/inventory/<int:item_id>")
def remove_inventory_item(item_id):
    """Delete an inventory item."""
    item = delete_item(item_id)

    if item is None:
        return jsonify({"error": "Inventory item not found."}), 404

    return jsonify({
        "message": "Inventory item deleted successfully.",
        "item": item,
    }), 200


# -------------------------
# OpenFoodFacts endpoints
# -------------------------

@app.get("/products/barcode/<barcode>")
def lookup_product_by_barcode(barcode):
    """Look up an external product by barcode."""
    try:
        product = find_product_by_barcode(barcode)

        if product is None:
            return jsonify({"error": "Product not found."}), 404

        return jsonify(product), 200

    except ValueError as error:
        return jsonify({"error": str(error)}), 400

    except requests.RequestException:
        return jsonify({
            "error": "OpenFoodFacts is unavailable."
        }), 502

    except (TypeError, KeyError):
        return jsonify({
            "error": "Invalid response from OpenFoodFacts."
        }), 502


@app.get("/products/search")
def lookup_products_by_name():
    """Search OpenFoodFacts products by name."""
    name = request.args.get("name", "").strip()

    if not name:
        return jsonify({
            "error": "Provide a product name using ?name=..."
        }), 400

    try:
        products = search_products_by_name(name)
        return jsonify({"products": products}), 200

    except ValueError as error:
        return jsonify({"error": str(error)}), 400

    except requests.RequestException:
        return jsonify({
            "error": "OpenFoodFacts is unavailable."
        }), 502

    except (TypeError, KeyError):
        return jsonify({
            "error": "Invalid response from OpenFoodFacts."
        }), 502


if __name__ == "__main__":
    app.run(debug=True)
