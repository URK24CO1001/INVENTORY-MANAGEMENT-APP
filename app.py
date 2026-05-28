from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# Create database table
def init_db():
    conn = sqlite3.connect('inventory.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            price REAL NOT NULL
        )
    ''')

    conn.commit()
    conn.close()

# Home page
@app.route('/')
def index():
    conn = sqlite3.connect('inventory.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()

    conn.close()

    return render_template('index.html', products=products)

# Add product
@app.route('/add', methods=['POST'])
def add_product():
    name = request.form['name']
    quantity = request.form['quantity']
    price = request.form['price']

    conn = sqlite3.connect('inventory.db')
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO products (name, quantity, price) VALUES (?, ?, ?)",
        (name, quantity, price)
    )

    conn.commit()
    conn.close()

    return redirect('/')

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
