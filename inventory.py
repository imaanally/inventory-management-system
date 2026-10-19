
# Mock inventory storage
inventory = [
    {
        "id": 1,
        "name": "Organic Almond Milk",
        "brand": "Silk",
        "barcode": "0123456789012",
        "quantity": 20,
        "price": 450.00,
        "category": "Beverages",
    },
    {
        "id": 2,
        "name": "Whole Wheat Bread",
        "brand": "Nature's Own",
        "barcode": "0761000601001",
        "quantity": 15,
        "price": 180.00,
        "category": "Bakery",
    },
]

def get_all_items():
    """Return all inventory items."""
    return inventory


def get_item_by_id(item_id):
    """Find an inventory item by its ID."""
    return next(
        (item for item in inventory if item["id"] == item_id),
        None,
    )


def add_item(item_data):
    """Add a new item and assign it a unique ID."""
    new_id = max((item["id"] for item in inventory), default=0) + 1

    new_item = {
        "id": new_id,
        **item_data,
    }

    inventory.append(new_item)
    return new_item


def update_item(item_id, updates):
    """Update selected fields on an existing item."""
    item = get_item_by_id(item_id)

    if item is None:
        return None

    item.update(updates)
    return item


def delete_item(item_id):
    """Delete an item and return it, or None if not found."""
    item = get_item_by_id(item_id)

    if item is None:
        return None

    inventory.remove(item)
    return item
