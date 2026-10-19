
import requests

BASE_URL = "https://world.openfoodfacts.org"
HEADERS = {
    "User-Agent": "InventoryManagementSystem/1.0 (educational project)"
}

PRODUCT_FIELDS = (
    "code,product_name,brands,ingredients_text,categories"
)


def normalize_product(product):
    """Return only the product details our inventory app needs."""
    return {
        "barcode": product.get("code", ""),
        "name": product.get("product_name", ""),
        "brand": product.get("brands", ""),
        "ingredients": product.get("ingredients_text", ""),
        "category": product.get("categories", ""),
    }


def find_product_by_barcode(barcode):
    """Fetch a product from OpenFoodFacts using its barcode."""
    if not isinstance(barcode, str) or not barcode.strip():
        raise ValueError("Barcode must be a non-empty string.")

    url = f"{BASE_URL}/api/v2/product/{barcode.strip()}"
    response = requests.get(
        url,
        params={"fields": PRODUCT_FIELDS},
        headers=HEADERS,
        timeout=10,
    )
    response.raise_for_status()

    data = response.json()

    if data.get("status") != 1 or not data.get("product"):
        return None

    return normalize_product(data["product"])


def search_products_by_name(name):
    """Search OpenFoodFacts for products matching a name."""
    if not isinstance(name, str) or not name.strip():
        raise ValueError("Product name must be a non-empty string.")

    url = f"{BASE_URL}/cgi/search.pl"
    response = requests.get(
        url,
        params={
            "search_terms": name.strip(),
            "search_simple": 1,
            "action": "process",
            "json": 1,
            "page_size": 10,
            "fields": PRODUCT_FIELDS,
        },
        headers=HEADERS,
        timeout=10,
    )
    response.raise_for_status()

    data = response.json()

    return [
        normalize_product(product)
        for product in data.get("products", [])
        if product.get("product_name")
    ]
