from flask import Flask, render_template, url_for, request, session, redirect, sessions
import sqlite3
import hashlib
import os
from Utilities.encryption import encrypt, decrypt
from Utilities.password import isValid

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
    if session:
        conn = get_db_connection()
        data = conn.execute("select * from passwords where username=? ",(session['username'],)).fetchall()
        for i in range(len(data)):
            data[i] = list(data[i])
            data[i][4] = decrypt(data[i][4])
        conn.close()
        return render_template('manage.html', entries=data)
    else:
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
                session['logged_in'] = True
                session['username'] = username
                return render_template('manage.html')
            else:
                print("Login failed")
        except Exception as e:
                print(str(e))
                msg = "Sign In Unsuccessful!"
                return redirect('/')

    return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method=='POST':
        username = request.form['username']
        password = request.form['password']
        emailid = request.form['email']
        
        try:
            flag, err = isValid(password)
            if not flag:
                return render_template('signup.html', alert_message=err)
            conn = get_db_connection()
            salt = os.urandom(32)
            plaintext = password.encode()
            digest = hashlib.pbkdf2_hmac('sha256', plaintext, salt, 10000)
            hashed_pwd = digest.hex()
            conn.execute("INSERT INTO users(username, hpassword, emailid, salt) VALUES(?,?,?,?)", (username, hashed_pwd, emailid, salt,))
            conn.commit()
            conn.close()
            return render_template('index.html')
            
        except Exception as e:
            print(str(e))
            msg = "Sign Up Unsuccessful!"
            return redirect('/')

    return render_template('signup.html')

@app.route('/logout')
def logout():
    session.clear()
    return render_template('index.html')

@app.route('/strengthchecker')
def strengthchecker():
    return render_template('strength-checker.html')

@app.route('/addnew', methods=['GET', 'POST'])
def addnew():
    if request.method=='POST':
        website = request.form['website']
        link = request.form['link']
        username = request.form['username']
        password = request.form['password']

        try:
            password = encrypt(password)
            conn = get_db_connection()
            conn.execute(" INSERT INTO passwords(username, website, webusername, link, password) VALUES(?,?,?,?,?)",  (session['username'], website,username, link, password,))
            conn.commit()
            conn.close()
            return redirect("/")
        except:
            pass

    return render_template('addnew.html')

@app.route('/delete_entry', methods=['GET', 'POST'])
def delete_entry():
    if request.method=='POST':
        web_username = request.form['web_username']
        website_name = request.form['website_name']

        try:
            conn = get_db_connection()
            conn.execute("DELETE FROM passwords WHERE webusername=? and website = ?",(web_username,website_name,))
            conn.commit()
            conn.close()
        except:
            pass

    return render_template('addnew.html')

# ansh123, ansh@gmail.com, anshu123

#---------------------------------------- Main ----------------------------------------#
if __name__ == "__main__":
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
    app.run(debug=True)