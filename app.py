from flask import Flask, render_template, request, url_for, redirect, session
import os
import sqlite3
import threading
import secrets
from script import ImageDownloader as pi

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)
main_directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), "images/")

# Create a thread-local storage for the SQLite connection
thread_local = threading.local()


def get_db():
    # Get the SQLite connection for the current thread
    if not hasattr(thread_local, 'connection'):
        thread_local.connection = sqlite3.connect('database.db')
    return thread_local.connection


def get_cursor():
    # Get the SQLite cursor for the current thread
    db = get_db()
    if not hasattr(thread_local, 'cursor'):
        thread_local.cursor = db.cursor()
    return thread_local.cursor


# Create a connection to the SQLite database
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Create a table for storing user registration data
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        firstname TEXT NOT NULL,
        lastname TEXT NOT NULL,
        email TEXT NOT NULL,
        password TEXT NOT NULL
    )
''')
conn.commit()


@app.route('/', methods=['GET', 'POST'])
def home():
    login_error = ""
    register_error = ""

    if 'user_id' in session:
        return redirect(url_for('download'))

    if request.method == 'POST':
        if 'login_submit' in request.form:
            email = request.form['login_email']
            password = request.form['login_password']

            if email and password:
                Cursor = get_cursor()
                Cursor.execute('SELECT id, email, password FROM users WHERE email = ? AND password = ?',
                               (email, password))
                result = Cursor.fetchone()

                if result:
                    user_id, email_from_db, password_from_db = result
                    if email == email_from_db and password == password_from_db:
                        session['user_id'] = user_id
                        return redirect(url_for('download'))
                    else:
                        login_error = "Invalid email or password"
                else:
                    login_error = "Invalid email or password"
            else:
                login_error = "Email and password are required"

        elif 'register_submit' in request.form:
            firstname = request.form['register_firstname']
            lastname = request.form['register_lastname']
            email = request.form['register_email']
            password = request.form['register_password']

            if firstname and lastname and email and password:
                Cursor = get_cursor()
                Cursor.execute('SELECT email FROM users WHERE email = ?', (email,))
                result = Cursor.fetchone()
                if result is not None and result[0] == email:
                    register_error = f"This {email} is already used by another user"
                else:
                    Cursor.execute('''
                        INSERT INTO users (firstname, lastname, email, password)
                        VALUES (?, ?, ?, ?)
                    ''', (firstname, lastname, email, password))
                    get_db().commit()
                    session['user_id'] = Cursor.lastrowid
                    return redirect(url_for('download'))
            else:
                register_error = "All fields are required"

    return render_template('home.html', login_error=login_error, register_error=register_error)


@app.route('/download', methods=['GET', 'POST'])
def download():
    if 'user_id' not in session:
        return redirect(url_for('home'))

    if request.method == 'POST':
        name = request.form.get('name')
        limit = int(request.form.get('limit'))
        if name:
            P = pi()
            P.download(name, limit=limit)
            return render_template('output.html')
        else:
            return "Invalid form data. Please provide a 'name' field."

    return render_template('index.html')


if __name__ == '__main__':
    app.debug = True
    app.run()
