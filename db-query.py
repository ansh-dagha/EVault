import sqlite3

db_local = 'users.db'
conn = sqlite3.connect(db_local)
c = conn.cursor()

c.execute(""" SELECT * FROM users
""")
print(c.fetchall())

#c.execute(""" DROP TABLE users """)

conn.commit()
conn.close()