"""Create and seed the local ecommerce SQLite database."""

import random
import sqlite3
from datetime import date, timedelta
from pathlib import Path

import pandas as pd


DATABASE_PATH = Path(__file__).resolve().parents[1] / "data" / "store.db"
RECORD_COUNT = 100

FIRST_NAMES = [
    "Olivia", "Liam", "Emma", "Noah", "Ava", "Oliver", "Sophia", "Elijah",
    "Isabella", "Lucas", "Mia", "Mason", "Amelia", "Ethan", "Harper", "James",
    "Evelyn", "Benjamin", "Abigail", "Henry",
]
LAST_NAMES = [
    "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller",
    "Davis", "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez",
    "Wilson", "Anderson", "Thomas", "Taylor", "Moore", "Jackson", "Martin",
]
LOCATIONS = [
    ("Seattle", "WA"),
    ("Austin", "TX"),
    ("Denver", "CO"),
    ("Boston", "MA"),
    ("Portland", "OR"),
    ("Chicago", "IL"),
    ("Atlanta", "GA"),
    ("San Diego", "CA"),
    ("Nashville", "TN"),
    ("Raleigh", "NC"),
]
PRODUCTS = [
    ("Wireless Headphones", "Electronics", 59.99, 149.99),
    ("Ceramic Coffee Mug", "Home & Kitchen", 12.00, 28.00),
    ("Cotton T-Shirt", "Clothing", 18.00, 45.00),
    ("Stainless Water Bottle", "Sports & Outdoors", 20.00, 42.00),
    ("Desk Lamp", "Home & Kitchen", 32.00, 85.00),
    ("Running Shoes", "Clothing", 65.00, 140.00),
    ("Bluetooth Speaker", "Electronics", 35.00, 110.00),
    ("Yoga Mat", "Sports & Outdoors", 22.00, 58.00),
    ("Cookbook", "Books", 16.00, 38.00),
    ("Backpack", "Accessories", 38.00, 120.00),
]
ORDER_STATUSES = ["delivered", "delivered", "delivered", "shipped", "processing", "cancelled"]


def create_mock_data() -> tuple[pd.DataFrame, pd.DataFrame]:
    """Build reproducible customer and order records."""
    rng = random.Random(42)
    customers = []

    for customer_id in range(1, RECORD_COUNT + 1):
        first_name = rng.choice(FIRST_NAMES)
        last_name = rng.choice(LAST_NAMES)
        city, state = rng.choice(LOCATIONS)
        signup_date = date(2022, 1, 1) + timedelta(days=rng.randint(0, 3 * 365))
        customers.append(
            {
                "customer_id": customer_id,
                "first_name": first_name,
                "last_name": last_name,
                "email": f"{first_name.lower()}.{last_name.lower()}.{customer_id}@example.com",
                "city": city,
                "state": state,
                "country": "United States",
                "signup_date": signup_date.isoformat(),
            }
        )

    orders = []
    earliest_order_date = date(2023, 1, 1)
    latest_order_date = date(2025, 12, 31)
    for order_id in range(1, RECORD_COUNT + 1):
        customer = rng.choice(customers)
        signup_date = date.fromisoformat(customer["signup_date"])
        first_order_day = max(signup_date, earliest_order_date)
        days_available = (latest_order_date - first_order_day).days
        order_date = first_order_day + timedelta(days=rng.randint(0, days_available))
        product_name, category, min_price, max_price = rng.choice(PRODUCTS)
        quantity = rng.choices([1, 2, 3, 4], weights=[65, 23, 9, 3])[0]
        unit_price = round(rng.uniform(min_price, max_price), 2)
        orders.append(
            {
                "order_id": order_id,
                "customer_id": customer["customer_id"],
                "order_date": order_date.isoformat(),
                "product_name": product_name,
                "category": category,
                "quantity": quantity,
                "unit_price": unit_price,
                "total_amount": round(quantity * unit_price, 2),
                "status": rng.choice(ORDER_STATUSES),
            }
        )

    return pd.DataFrame(customers), pd.DataFrame(orders)


def create_database(database_path: Path = DATABASE_PATH) -> None:
    """Create the database schema and replace its mock records."""
    database_path.parent.mkdir(parents=True, exist_ok=True)
    customers, orders = create_mock_data()

    with sqlite3.connect(database_path) as connection:
        connection.execute("PRAGMA foreign_keys = ON")
        connection.executescript(
            """
            CREATE TABLE IF NOT EXISTS customers (
                customer_id INTEGER PRIMARY KEY,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                city TEXT NOT NULL,
                state TEXT NOT NULL,
                country TEXT NOT NULL,
                signup_date TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS orders (
                order_id INTEGER PRIMARY KEY,
                customer_id INTEGER NOT NULL,
                order_date TEXT NOT NULL,
                product_name TEXT NOT NULL,
                category TEXT NOT NULL,
                quantity INTEGER NOT NULL CHECK (quantity > 0),
                unit_price REAL NOT NULL CHECK (unit_price >= 0),
                total_amount REAL NOT NULL CHECK (total_amount >= 0),
                status TEXT NOT NULL,
                FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
            );
            """
        )
        connection.execute("DELETE FROM orders")
        connection.execute("DELETE FROM customers")
        customers.to_sql("customers", connection, if_exists="append", index=False)
        orders.to_sql("orders", connection, if_exists="append", index=False)

    print(f"Created {database_path} with {len(customers)} customers and {len(orders)} orders.")


if __name__ == "__main__":
    create_database()