# Inventory Management System

A Python-based inventory management system built with Flask. It provides a REST API and an interactive command-line interface (CLI) for managing inventory items, with product lookup functionality powered by the OpenFoodFacts API.

## Features

- View all inventory items and retrieve individual items.
- Add new inventory items.
- Update product prices and stock quantities.
- Delete inventory items.
- Search for products by barcode or product name using OpenFoodFacts.
- Add products found through OpenFoodFacts to the local inventory.
- Validate input data and return appropriate HTTP error responses.
- Automated tests using pytest and mocked external API requests.

## Technologies Used

- Python 3.12
- Flask
- Requests
- OpenFoodFacts API
- pytest
- unittest.mock
- Git and GitHub

## Project Structure

```text
inventory-management-system/
├── app.py
├── cli.py
├── inventory.py
├── openfoodfacts.py
├── requirements.txt
├── README.md
└── tests/
    ├── __init__.py
    ├── test_api.py
    ├── test_cli.py
    ├── test_openfoodfacts.py
    └── test_product_routes.py
```

## Installation and Setup

### 1. Clone the repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd inventory-management-system
```

Replace `<YOUR_GITHUB_REPOSITORY_URL>` with the URL of your GitHub repository.

### 2. Create a virtual environment

```bash
python3 -m venv .venv
```

### 3. Activate the virtual environment

On Linux or Ubuntu:

```bash
source .venv/bin/activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

## Running the Application

### Start the Flask API

In your first terminal, run:

```bash
python app.py
```

The development server runs at:

`http://127.0.0.1:5000`

Keep this terminal open while using the CLI.

### Start the CLI

Open a second terminal, navigate to the project directory, and activate the virtual environment:

```bash
cd inventory-management-system
source .venv/bin/activate
python cli.py
```

Use the interactive menu to view, add, update, delete, and search for inventory products.

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/inventory` | Retrieve all inventory items |
| GET | `/inventory/<id>` | Retrieve one item by ID |
| POST | `/inventory` | Create an inventory item |
| PATCH | `/inventory/<id>` | Update an item's fields |
| DELETE | `/inventory/<id>` | Delete an inventory item |
| GET | `/products/barcode/<barcode>` | Find a product by barcode |
| GET | `/products/search?name=<name>` | Search products by name |

### Example: Retrieve all inventory items

```bash
curl http://127.0.0.1:5000/inventory
```

### Example: Retrieve one item

```bash
curl http://127.0.0.1:5000/inventory/1
```

### Example: Add an inventory item

```bash
curl -X POST http://127.0.0.1:5000/inventory \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Mango Juice",
    "brand": "Del Monte",
    "barcode": "1234567890123",
    "category": "Beverages",
    "quantity": 10,
    "price": 150
  }'
```

The required fields are `name`, `quantity`, and `price`. Other supported fields are `brand`, `barcode`, and `category`.

### Example: Update stock quantity

```bash
curl -X PATCH http://127.0.0.1:5000/inventory/1 \
  -H "Content-Type: application/json" \
  -d '{"quantity": 25}'
```

### Example: Delete an item

```bash
curl -X DELETE http://127.0.0.1:5000/inventory/1
```

### Example: Search OpenFoodFacts by barcode

```bash
curl http://127.0.0.1:5000/products/barcode/3017620422003
```

### Example: Search OpenFoodFacts by product name

```bash
curl --get http://127.0.0.1:5000/products/search \
  --data-urlencode "name=Green Tea"
```

OpenFoodFacts requires an internet connection. Search results depend on the data available from the external service.

## Running the Tests

Activate the virtual environment, then run:

```bash
pytest -v
```

The tests cover:

- Inventory API CRUD operations and validation.
- CLI operations using mocked HTTP requests.
- OpenFoodFacts product lookup and error handling.
- Flask routes for external product searches.

External HTTP requests are mocked in automated tests so the tests do not depend on the live OpenFoodFacts service.

## Data Storage

Inventory items are currently stored in an in-memory Python list. Changes are not persisted after the Flask application restarts. A database can be added as a future enhancement.

## Future Improvements

- Persistent storage using SQLite or PostgreSQL.
- User authentication and authorization.
- Stock alerts for low inventory.
- Improved reporting and inventory summaries.

## Author

Developed as a software engineering summative project.
