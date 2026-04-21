import sqlite3
import os
from werkzeug.security import generate_password_hash

DB = "mini_amazon.db"


def get_db():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    c = conn.cursor()

    # Users
    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id       INTEGER PRIMARY KEY AUTOINCREMENT,
            name     TEXT NOT NULL,
            email    TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            is_admin INTEGER DEFAULT 0
        )
    """)

    # Products
    c.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            name        TEXT NOT NULL,
            description TEXT,
            price       REAL NOT NULL,
            stock       INTEGER DEFAULT 10,
            category    TEXT,
            image_url   TEXT
        )
    """)

    # Orders
    c.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id         INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id    INTEGER,
            total      REAL,
            status     TEXT DEFAULT 'Pending',
            created_at TEXT DEFAULT (datetime('now')),
            name       TEXT,
            address    TEXT,
            phone      TEXT,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    """)

    # Order Items
    c.execute("""
        CREATE TABLE IF NOT EXISTS order_items (
            id         INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id   INTEGER,
            product_id INTEGER,
            quantity   INTEGER,
            price      REAL,
            FOREIGN KEY(order_id)   REFERENCES orders(id),
            FOREIGN KEY(product_id) REFERENCES products(id)
        )
    """)

    conn.commit()

    # Seed admin user
    existing = c.execute("SELECT id FROM users WHERE email='admin@shop.com'").fetchone()
    if not existing:
        c.execute("INSERT INTO users (name, email, password, is_admin) VALUES (?,?,?,?)",
                  ("Admin", "admin@shop.com", generate_password_hash("admin123"), 1))

    # Seed sample products
    count = c.execute("SELECT COUNT(*) FROM products").fetchone()[0]
    if count == 0:
        products = [
            ("Wireless Headphones",  "Premium sound quality with noise cancellation", 2499.00, 15, "Electronics",  "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=300"),
            ("Running Shoes",        "Lightweight and breathable sport shoes",          1799.00, 20, "Footwear",     "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=300"),
            ("Backpack 30L",         "Durable travel backpack with laptop sleeve",      1299.00, 25, "Bags",         "https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=300"),
            ("Smart Watch",          "Fitness tracker with heart rate monitor",         3999.00, 8,  "Electronics",  "https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=300"),
            ("Sunglasses",           "UV400 polarised sunglasses",                       799.00, 30, "Accessories",  "https://images.unsplash.com/photo-1572635196237-14b3f281503f?w=300"),
            ("Mechanical Keyboard",  "RGB backlit mechanical gaming keyboard",          4499.00, 10, "Electronics",  "https://images.unsplash.com/photo-1511467687858-23d96c32e4ae?w=300"),
            ("Water Bottle 1L",      "Insulated stainless steel bottle",                 599.00, 40, "Accessories",  "https://images.unsplash.com/photo-1602143407151-7111542de6e8?w=300"),
            ("Desk Lamp LED",        "Adjustable colour temperature desk lamp",          899.00, 18, "Home",         "https://images.unsplash.com/photo-1507473885765-e6ed057f782c?w=300"),
        ]
        c.executemany("INSERT INTO products (name,description,price,stock,category,image_url) VALUES (?,?,?,?,?,?)", products)

    conn.commit()
    conn.close()
    print("✅ Database ready.")