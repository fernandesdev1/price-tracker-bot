import sqlite3
from datetime import datetime
from typing import List, Optional
from tracker.models import Product, PricePoint

class SQLiteStorage:
    def __init__(self, db_path: str = "db.sqlite3"):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        with sqlite3.connect(self.db_path, timeout=20) as conn:
            cursor = conn.cursor()
            cursor.execute("PRAGMA journal_mode=WAL") # Melhora a concorrência
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS products (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    url TEXT UNIQUE NOT NULL,
                    current_price REAL,
                    last_updated TIMESTAMP
                )
            ''')
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS price_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    product_id INTEGER,
                    price REAL NOT NULL,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (product_id) REFERENCES products (id)
                )
            ''')
            conn.commit()

    def add_product(self, product: Product) -> int:
        with sqlite3.connect(self.db_path, timeout=20) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT OR IGNORE INTO products (name, url, current_price, last_updated) VALUES (?, ?, ?, ?)",
                (product.name, product.url, product.current_price, product.last_updated)
            )
            product_id = cursor.lastrowid
            
            if product_id == 0:
                cursor.execute("SELECT id FROM products WHERE url = ?", (product.url,))
                product_id = cursor.fetchone()[0]
            
            if product.current_price is not None:
                # Inserindo direto na mesma conexão pra não dar erro de lock
                cursor.execute(
                    "INSERT INTO price_history (product_id, price, timestamp) VALUES (?, ?, ?)",
                    (product_id, product.current_price, datetime.now())
                )
                cursor.execute(
                    "UPDATE products SET current_price = ?, last_updated = ? WHERE id = ?",
                    (product.current_price, datetime.now(), product_id)
                )
            
            conn.commit()
            return product_id

    def add_price_history(self, product_id: int, price: float):
        # Esse método continua aqui pra casos de update avulso
        with sqlite3.connect(self.db_path, timeout=20) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO price_history (product_id, price, timestamp) VALUES (?, ?, ?)",
                (product_id, price, datetime.now())
            )
            cursor.execute(
                "UPDATE products SET current_price = ?, last_updated = ? WHERE id = ?",
                (price, datetime.now(), product_id)
            )
            conn.commit()

    def delete_product(self, product_id: int):
        with sqlite3.connect(self.db_path, timeout=20) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM price_history WHERE product_id = ?", (product_id,))
            cursor.execute("DELETE FROM products WHERE id = ?", (product_id,))
            conn.commit()

    def get_all_products(self) -> List[Product]:
        products_list = []
        with sqlite3.connect(self.db_path, timeout=20) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM products")
            rows = cursor.fetchall()
            
            for row in rows:
                p = Product(
                    id=row['id'],
                    name=row['name'],
                    url=row['url'],
                    current_price=row['current_price'],
                    last_updated=row['last_updated']
                )
                products_list.append(p)
        return products_list

    def get_price_history(self, product_id: int) -> List[PricePoint]:
        history = []
        with sqlite3.connect(self.db_path, timeout=20) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM price_history WHERE product_id = ? ORDER BY timestamp DESC", (product_id,))
            rows = cursor.fetchall()
            for row in rows:
                history.append(PricePoint(price=row['price'], timestamp=row['timestamp']))
        return history
