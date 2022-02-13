import sqlite3

db_local = 'users.db'
conn = sqlite3.connect(db_local)
c = conn.cursor()

# c.execute(""" INSERT INTO passwords(username, website, webusername, link, password) VALUES('ansh123', 'instagram', 'ansh.dagha', 'https://instagram.com', 'prachithebest')
# """)

#print(c.fetchall())

#c.execute(""" DROP TABLE users """)

c.execute(""" SELECT * FROM passwords """)
print(c.fetchall())
conn.commit()
conn.close()