import sqlite3

def promote_user():
    conn = sqlite3.connect('shop.db')
    c = conn.cursor()
    
    # This finds the very first person who registered (ID 1) 
    # and changes their role to 'admin'
    c.execute("UPDATE users SET role = 'admin' WHERE id = 1")
    
    conn.commit()
    conn.close()
    print("Success! User #1 is now an Admin.")

if __name__ == "__main__":
    promote_user()