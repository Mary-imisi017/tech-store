import sqlite3

def init_db():
    conn = sqlite3.connect('shop.db')
    c = conn.cursor()
    # Users table: Includes a 'role' column for Admin vs Customer
    c.execute('''CREATE TABLE IF NOT EXISTS users 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, email TEXT UNIQUE, password TEXT, role TEXT)''')
    # Products table
    c.execute('''CREATE TABLE IF NOT EXISTS products 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, price REAL)''')
    # Orders table
    c.execute('''CREATE TABLE IF NOT EXISTS orders 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER, product_name TEXT, total REAL)''')
    conn.commit()
    conn.close()
    print("Database initialized: shop.db created!")

if __name__ == "__main__":
    init_db()