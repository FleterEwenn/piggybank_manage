import sqlite3

conn = sqlite3.connect('userdb.db')
cur = conn.cursor()

response = True

while response:
  response = input('>>  ')
  cur.execute(response)
  cur.commit()
conn.close()
