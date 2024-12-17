from flask import Flask, render_template, request, redirect, flash
import sqlite3
from werkzeug.security import generate_password_hash

app = Flask(__name__)
app.secret_key = 'clave_secreta_segura'  


DB = "Login.db"

def init_db():
    with sqlite3.connect(DB) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            )
        """)
        conn.commit()

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        hashed_password = generate_password_hash(password)

        try:
            with sqlite3.connect(DB) as conn:
                cursor = conn.cursor()
                cursor.execute("INSERT INTO users (email, password) VALUES (?, ?)", (email, hashed_password))
                conn.commit()
                flash('Usuario registrado con éxito', 'success')
                return redirect('/register')
        except sqlite3.IntegrityError:
            flash('El correo ya está registrado', 'error')
    return render_template('registro.html')

if __name__ == '__main__':
    init_db()
    app.run(host="0.0.0.0", debug=True)
