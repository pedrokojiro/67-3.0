import sqlite3

DATABASE_NAME = "restaurante.db"

def get_connection():
    conn = sqlite3.connect(DATABASE_NAME)
    conn.execute("PRAGMA foreign_keys = ON;")
    conn.row_factory = sqlite3.Row
    return conn

def create_tables():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        role TEXT NOT NULL
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS addresses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        street TEXT NOT NULL,
        number TEXT NOT NULL,
        complement TEXT,
        city TEXT NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS categories (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        active BOOLEAN DEFAULT 1
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        price REAL NOT NULL,
        category_id INTEGER NOT NULL,
        description TEXT,
        FOREIGN KEY (category_id) REFERENCES categories (id)
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS option_groups (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        product_id INTEGER,
        name TEXT NOT NULL,
        min_options INTEGER DEFAULT 0,
        max_options INTEGER DEFAULT 1,
        FOREIGN KEY (product_id) REFERENCES products (id) ON DELETE CASCADE
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS coupons (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        code TEXT UNIQUE NOT NULL,
        discount_percentage REAL NOT NULL,
        active BOOLEAN DEFAULT 1
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tables (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        number INTEGER UNIQUE NOT NULL,
        status TEXT DEFAULT 'Livre'
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        total REAL NOT NULL,
        status TEXT DEFAULT 'Pendente',
        items_json TEXT,
        FOREIGN KEY (user_id) REFERENCES users (id)
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS payments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        order_id INTEGER NOT NULL,
        method TEXT NOT NULL,
        amount REAL NOT NULL,
        FOREIGN KEY (order_id) REFERENCES orders (id)
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS reviews (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        order_id INTEGER NOT NULL,
        rating INTEGER NOT NULL,
        comment TEXT,
        FOREIGN KEY (order_id) REFERENCES orders (id)
    );
    """)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_tables()