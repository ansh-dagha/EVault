import sqlite3
import hashlib
import os

db_local = 'users.db'
conn = sqlite3.connect(db_local)
c = conn.cursor()

salt = os.urandom(32)
plaintext = 'prapra123'.encode()

digest = hashlib.pbkdf2_hmac('sha256', plaintext, salt, 10000)

hashed_pwd = digest.hex()
print(hashed_pwd)

c.execute(""" INSERT INTO users(username, hpassword, emailid, salt) VALUES('pdr123',?, 'pdra2gmail.com', ?)
    """, (hashed_pwd, salt,))

#c.execute(""" DROP TABLE users """)

conn.commit()
conn.close()