from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)
DATABASE = "meat_store.db"




def create_table():
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS items (id INTEGER PRIMARY KEY, name TEXT, price REAL, supplier TEXT)")
    connection.commit()
    connection.close()


#create_table()


@app.route('/')
def index():
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM items")
    items = cursor.fetchall()
    connection.close()
    return render_template('index.html', items=items)


@app.route('/add_item', methods=['GET', 'POST'])
def add_item():
    if request.method == 'POST':
        name = request.form['name']
        price = request.form['price']
        supplier = request.form['supplier']
        connection = sqlite3.connect(DATABASE)
        cursor = connection.cursor()
        cursor.execute("INSERT INTO items (name, price, supplier) VALUES (?, ?, ?)", (name, price, supplier))
        connection.commit()
        connection.close()
        return redirect(url_for('index'))
    return render_template('add_item.html')


@app.route('/update_item/<int:item_id>', methods=['GET', 'POST'])
def update_item(item_id):
    if request.method == 'POST':
        name = request.form['name']
        price = request.form['price']
        supplier = request.form['supplier']
        weight = request.form['weight']
        connection = sqlite3.connect(DATABASE)
        cursor = connection.cursor()
        cursor.execute("UPDATE items SET name=?, price=?, supplier=?, weight=?  WHERE id=?", (name, price, supplier, item_id,weight))
        connection.commit()
        connection.close()
        return redirect(url_for('index'))
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM items WHERE id=?", (item_id,))
    item = cursor.fetchone()
    connection.close()
    return render_template('update_item.html', item=item)


@app.route('/delete_item/<int:item_id>')
def delete_item(item_id):
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()
    cursor.execute("DELETE FROM items WHERE id=?", (item_id,))
    connection.commit()
    connection.close()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
