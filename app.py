from flask import Flask, render_template, url_for, request, session, redirect
import sqlite3
import hashlib
import os

app = Flask(__name__)
app.secret_key = "super secret key"

def get_db_connection():
    conn = sqlite3.connect('users.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.after_request
def add_header(r):
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r

@app.route('/', methods=['GET', 'POST'])
def basic():
    return render_template('index.html')

@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method=='POST':
        username = request.form['username']
        password = request.form['password']
        
        try:
            conn = get_db_connection()
            user = conn.execute("select * from users where username=? ",(username,)).fetchone()
            conn.close()
            print(user)
            salt = user['salt']
            plaintext = password.encode()

            digest = hashlib.pbkdf2_hmac('sha256', plaintext, salt, 10000)

            hex_hash = digest.hex()
            print(hex_hash)
            if hex_hash == user['hpassword']:
                print("Login successful")
            else:
                print("Login failed")
        except Exception as e:
                print(str(e))
                msg = "Sign In Unsuccessful!"
                return redirect('/')

    return render_template('index.html')

#---------------------------------------- Main ----------------------------------------#
if __name__ == "__main__":
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
    app.run(debug=True)