
import requests

BASE_URL = "http://127.0.0.1:5000"


def view_inventory():
    try:
        response = requests.get(f"{BASE_URL}/inventory", timeout=10)
        response.raise_for_status()

        items = response.json()

        if not items:
            print("Your inventory is empty.")
            return

        print("\n--- INVENTORY ---")
        for item in items:
            print(
                f"ID: {item['id']} | "
                f"Name: {item['name']} | "
                f"Quantity: {item['quantity']} | "
                f"Price: {item['price']}"
            )

    except requests.RequestException as error:
        print(f"Could not connect to the inventory API: {error}")


def add_inventory_item():
    name = input("Product name: ").strip()
    brand = input("Brand (optional): ").strip()
    barcode = input("Barcode (optional): ").strip()
    category = input("Category (optional): ").strip()

    try:
        quantity = int(input("Quantity: "))
        price = float(input("Price: "))

        if quantity < 0 or price < 0:
            print("Quantity and price cannot be negative.")
            return

    except ValueError:
        print("Quantity must be a whole number and price must be numeric.")
        return

    if not name:
        print("Product name cannot be empty.")
        return

    item = {
        "name": name,
        "quantity": quantity,
        "price": price,
    }

    if brand:
        item["brand"] = brand
    if barcode:
        item["barcode"] = barcode
    if category:
        item["category"] = category

    try:
        response = requests.post(
            f"{BASE_URL}/inventory",
            json=item,
            timeout=10,
        )

        if response.status_code == 201:
            print("Item added successfully!")
            print(response.json())
        else:
            print(f"Could not add item: {response.text}")

    except requests.RequestException as error:
        print(f"Could not connect to the inventory API: {error}")


def update_inventory_item():
    try:
        item_id = int(input("Enter item ID: "))
        print("1. Update price")
        print("2. Update quantity")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            price = float(input("New price: "))
            if price < 0:
                print("Price cannot be negative.")
                return
            updates = {"price": price}

        elif choice == "2":
            quantity = int(input("New quantity: "))
            if quantity < 0:
                print("Quantity cannot be negative.")
                return
            updates = {"quantity": quantity}

        else:
            print("Invalid option.")
            return

    except ValueError:
        print("Enter a valid item ID and numeric value.")
        return

    try:
        response = requests.patch(
            f"{BASE_URL}/inventory/{item_id}",
            json=updates,
            timeout=10,
        )

        if response.status_code == 200:
            print("Item updated successfully!")
            print(response.json())
        else:
            print(f"Could not update item: {response.text}")

    except requests.RequestException as error:
        print(f"Could not connect to the inventory API: {error}")


def delete_inventory_item():
    try:
        item_id = int(input("Enter item ID to delete: "))
    except ValueError:
        print("Item ID must be a number.")
        return

    try:
        response = requests.delete(
            f"{BASE_URL}/inventory/{item_id}",
            timeout=10,
        )

        if response.status_code == 200:
            print("Item deleted successfully!")
        else:
            print(f"Could not delete item: {response.text}")

    except requests.RequestException as error:
        print(f"Could not connect to the inventory API: {error}")


def find_product():
    print("\n1. Search by barcode")
    print("2. Search by product name")

    choice = input("Choose an option: ").strip()

    try:
        if choice == "1":
            barcode = input("Enter barcode: ").strip()
            if not barcode:
                print("Barcode cannot be empty.")
                return

            response = requests.get(
                f"{BASE_URL}/products/barcode/{barcode}",
                timeout=15,
            )

            if response.status_code == 200:
                product = response.json()
                print("\nProduct found:")
                print(product)
                add_found_product(product)
            elif response.status_code == 404:
                print("Product not found.")
            else:
                print(f"Product lookup failed: {response.text}")

        elif choice == "2":
            name = input("Enter product name: ").strip()
            if not name:
                print("Product name cannot be empty.")
                return

            response = requests.get(
                f"{BASE_URL}/products/search",
                params={"name": name},
                timeout=15,
            )

            if response.status_code != 200:
                print(f"Product lookup failed: {response.text}")
                return

            products = response.json().get("products", [])

            if not products:
                print("No products found.")
                return

            for index, product in enumerate(products, start=1):
                print(
                    f"{index}. {product.get('name', 'Unknown')} | "
                    f"Brand: {product.get('brand', 'Unknown')} | "
                    f"Barcode: {product.get('barcode', 'Unknown')}"
                )

            selection = input(
                "Enter the number of the product to add, "
                "or press Enter to cancel: "
            ).strip()

            if not selection:
                return

            try:
                product_index = int(selection) - 1
                if not 0 <= product_index < len(products):
                    print("Invalid product number.")
                    return
            except ValueError:
                print("Enter a valid product number.")
                return

            add_found_product(products[product_index])

        else:
            print("Invalid option.")

    except requests.RequestException as error:
        print(f"Could not connect to the API: {error}")


def add_found_product(product):
    confirmation = input(
        "Add this product to inventory? (y/n): "
    ).strip().lower()

    if confirmation != "y":
        print("Product not added.")
        return

    name = product.get("name", "").strip()

    if not name:
        print("This product has no name and cannot be added.")
        return

    item = {
        "name": name,
        "brand": product.get("brand", ""),
        "barcode": product.get("barcode", ""),
        "category": product.get("category", ""),
        "quantity": 0,
        "price": 0,
    }

    try:
        response = requests.post(
            f"{BASE_URL}/inventory",
            json=item,
            timeout=10,
        )

        if response.status_code == 201:
            print("Product added to inventory!")
            print(response.json())
            print("Remember to update its price and stock quantity.")
        else:
            print(f"Could not add product: {response.text}")

    except requests.RequestException as error:
        print(f"Could not connect to the inventory API: {error}")


def main():
    while True:
        print("\n===== INVENTORY MANAGEMENT SYSTEM =====")
        print("1. View inventory")
        print("2. Add inventory item")
        print("3. Update price or quantity")
        print("4. Delete inventory item")
        print("5. Find product using OpenFoodFacts")
        print("6. Exit")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            view_inventory()
        elif choice == "2":
            add_inventory_item()
        elif choice == "3":
            update_inventory_item()
        elif choice == "4":
            delete_inventory_item()
        elif choice == "5":
            find_product()
        elif choice == "6":
            print("Goodbye!")
            break
        else:
            print("Invalid option. Please choose 1–6.")


if __name__ == "__main__":
    main()
