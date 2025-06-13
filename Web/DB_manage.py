import sqlite3
import hashlib

def insert_newuser(username : str, password : str):
    conn = sqlite3.connect('userdb.db')

    h_pass = hashlib.sha256()
    h_pass.update(password.encode())
    password_hash = h_pass.hexdigest()

    cur = conn.cursor()
    cur.execute("INSERT INTO User (username, password, money, color, listValue) VALUES  (?, ?, ?, ?, ?)", (username, password_hash, 0, '#9B59B6,black', ""))

    conn.commit()
    conn.close()

def signin_user(username : str, password : str):
    conn = sqlite3.connect('userdb.db')

    h_pass = hashlib.sha256()
    h_pass.update(password.encode())
    password_hash = h_pass.hexdigest()

    cur = conn.cursor()
    res = cur.execute("SELECT id, color FROM User WHERE username=? AND password=?", (username, password_hash)).fetchall()

    conn.commit()
    conn.close()
    return res