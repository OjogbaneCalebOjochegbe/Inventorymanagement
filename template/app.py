from flask import Flask, render_template, request, redirect
import mysql.connector

app = Flask(__name__)

# DB Connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="book_inventory"
)
cursor = db.cursor(dictionary=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        search = request.form['search']
        cursor.execute("SELECT * FROM books WHERE name LIKE %s", ('%' + search + '%',))
    else:
        cursor.execute("SELECT * FROM books")
    books = cursor.fetchall()
    return render_template('index.html', books=books)

@app.route('/add', methods=['GET', 'POST'])
def add_book():
    if request.method == 'POST':
        name = request.form['name']
        bookType = request.form['bookType']
        quantity = request.form['quantity']
        price = request.form['price']
        cursor.execute("INSERT INTO drinks (name, bookType, quantity, price) VALUES (%s, %s, %s, %s)", 
                       (name, bookType, quantity, price))
        db.commit()
        return redirect('/')
    return render_template('add.html')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_book(id):
    if request.method == 'POST':
        name = request.form['name']
        bookType = request.form['bookType']
        quantity = request.form['quantity']
        price = request.form['price']
        cursor.execute("UPDATE drinks SET name=%s, bookType=%s, quantity=%s, price=%s WHERE id=%s", 
                       (name, bookType, quantity, price, id))
        db.commit()
        return redirect('/')
    cursor.execute("SELECT * FROM books WHERE id=%s", (id,))
    book = cursor.fetchone()
    return render_template('edit.html', book=book)


@app.route('/delete/<int:id>')
def delete_drink(id):
    cursor.execute("DELETE FROM Books WHERE id=%s", (id,))
    db.commit()
    return redirect('/')