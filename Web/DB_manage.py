import sqlite3

def recup(username, password):
    conn = sqlite3.connect('userdb.db')

    cur = conn.cursor()
    cur.execute("INSERT INTO User VALUES username=?, password=?, money=?, color=? ", (username, password, 0, '#9B59B6,black'))

    conn.commit()
    conn.close()

    return True
