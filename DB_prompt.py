import sqlite3

conn = sqlite3.connect('userdb.db')
cur = conn.cursor()

response = True

while response:
  response = input('>> ')
  print(cur.execute(response).fetchall())
  conn.commit()
conn.close()
