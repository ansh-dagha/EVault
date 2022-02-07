import sqlite3

db_local = 'users.db'
conn = sqlite3.connect(db_local)
c = conn.cursor()

c.execute(""" CREATE TABLE users
(
username TEXT PRIMARY KEY , hpassword TEXT, emailid TEXT, salt TEXT
)
""")

#c.execute(""" DROP TABLE users """)

conn.commit()
conn.close()