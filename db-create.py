import sqlite3

db_local = 'users.db'
conn = sqlite3.connect(db_local)
c = conn.cursor()

# c.execute(""" CREATE TABLE users
# (
# username TEXT PRIMARY KEY , hpassword TEXT, emailid TEXT, salt TEXT
# )
# """)

c.execute(""" CREATE TABLE passwords
(
username TEXT , website TEXT , webusername TEXT, link TEXT, password TEXT NOT NULL, PRIMARY KEY (website, webusername) 
)
""")

#c.execute(""" DROP TABLE users """)

conn.commit()
conn.close()