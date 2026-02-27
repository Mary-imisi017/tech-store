from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3

app = Flask(__name__)
app.secret_key = "very_secret_key"

def get_db():
    conn = sqlite3.connect('shop.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def home():
    db = get_db()
    items = db.execute('SELECT * FROM products').fetchall()
    return render_template('products.html', products=items)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name, email, pwd = request.form['name'], request.form['email'], request.form['password']
        db = get_db()
        try:
            db.execute('INSERT INTO users (name, email, password, role) VALUES (?, ?, ?, ?)', 
                       (name, email, pwd, 'customer'))
            db.commit()
            return redirect(url_for('login'))
        except: return "Email already exists!"
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email, pwd = request.form['email'], request.form['password']
        db = get_db()
        user = db.execute('SELECT * FROM users WHERE email=? AND password=?', (email, pwd)).fetchone()
        if user:
            session['user_id'], session['user_name'], session['role'] = user['id'], user['name'], user['role']
            return redirect(url_for('admin' if user['role'] == 'admin' else 'home'))
    return render_template('login.html')

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if session.get('role') != 'admin': return "Access Denied!"
    db = get_db()
    if request.method == 'POST':
        db.execute('INSERT INTO products (name, price) VALUES (?, ?)', 
                   (request.form['name'], request.form['price']))
        db.commit()
    orders = db.execute('SELECT * FROM orders').fetchall()
    return render_template('admin.html', orders=orders)


@app.route('/delete-product/<int:product_id>', methods=['POST'])
def delete_product(product_id):
    if session.get('role') != 'admin':
        return "Unauthorized", 403
    
    db = get_db()
    db.execute('DELETE FROM products WHERE id = ?', (product_id,))
    db.commit()
    return redirect(url_for('admin_dashboard')) # Or whatever your admin route is called

@app.route('/buy/<int:product_id>', methods=['POST']) # Make sure POST is here!
def buy_product(product_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    db = get_db()
    product = db.execute('SELECT * FROM products WHERE id = ?', (product_id,)).fetchone()
    
    if product:
        db.execute('INSERT INTO orders (user_id, product_name, total) VALUES (?, ?, ?)',
                   (session['user_id'], product['name'], product['price']))
        db.commit()
        # Make sure you are redirecting to the success page
        return render_template('success.html') 
    
    return redirect(url_for('index'))
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)