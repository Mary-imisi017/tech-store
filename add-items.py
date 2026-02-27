import sqlite3

def add_test_data():
    conn = sqlite3.connect('shop.db')
    c = conn.cursor()
    
    # Adding a few products to make the shop look full
    products = [
        ('Gaming Laptop', 1200.00),
        ('Wireless Mouse', 25.50),
        ('Mechanical Keyboard', 85.00),
        ('Monitor 24 inch', 150.00)
    ]
    
    c.executemany("INSERT INTO products (name, price) VALUES (?, ?)", products)
    
    conn.commit()
    conn.close()
    print("Successfully added 4 products to the shop!")

if __name__ == "__main__":
    add_test_data()