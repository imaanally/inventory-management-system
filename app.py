
from flask import Flask, jsonify, request

from inventory import (
    add_item,
    delete_item,
    get_all_items,
    get_item_by_id,
    update_item,
)

app = Flask(__name__)

# Fields employees are allowed to store or update.
ALLOWED_FIELDS = {
    "name",
    "brand",
    "barcode",
    "quantity",
    "price",
    "category",
}


def validate_item_data(data, partial=False):
    """Validate inventory fields and return an error message if invalid."""
    if not isinstance(data, dict):
        return "Request body must be a JSON object."

    if not partial:
        missing = {"name", "quantity", "price"} - data.keys()
        if missing:
            return f"Missing required fields: {', '.join(sorted(missing))}"

    unknown = data.keys() - ALLOWED_FIELDS
    if unknown:
        return f"Unknown fields: {', '.join(sorted(unknown))}"

    for field in ("name", "brand", "barcode", "category"):
        if field in data and (
            not isinstance(data[field], str) or not data[field].strip()
        ):
            return f"{field} must be a non-empty string."

    for field in ("quantity", "price"):
        if field in data:
            value = data[field]

            if isinstance(value, bool) or not isinstance(value, (int, float)):
                return f"{field} must be a number."

            if field == "quantity" and (
                not isinstance(value, int) or value < 0
            ):
                return "quantity must be a non-negative integer."

            if field == "price" and value < 0:
                return "price must be non-negative."

    if partial and not data:
        return "Provide at least one field to update."

    return None


@app.get("/inventory")
def list_inventory():
    """Return all inventory items."""
    return jsonify(get_all_items()), 200


@app.get("/inventory/<int:item_id>")
def get_inventory_item(item_id):
    """Return one inventory item."""
    item = get_item_by_id(item_id)

    if item is None:
        return jsonify({"error": "Inventory item not found."}), 404

    return jsonify(item), 200


@app.post("/inventory")
def create_inventory_item():
    """Create an inventory item."""
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


if __name__ == "__main__":
    app.run(debug=True)
