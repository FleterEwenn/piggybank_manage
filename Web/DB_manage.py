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

def signin_user_forweb(username : str, password : str):
    conn = sqlite3.connect('userdb.db')

    h_pass = hashlib.sha256()
    h_pass.update(password.encode())
    password_hash = h_pass.hexdigest()

    cur = conn.cursor()
    user_table_db = cur.execute("SELECT id, color FROM User WHERE username = ? AND password = ?", (username, password_hash))
    user_table = user_table_db.fetchall()

    conn.close()
    
    if user_table != []:
        return user_table
    else:
        return None

def signin_user_forapp(username : str, password : str):
    conn = sqlite3.connect('userdb.db')

    cur = conn.cursor()
    user_table_db = cur.execute("SELECT id, username, password, money, color, listValue FROM User WHERE username = ? AND password = ?", (username, password))
    user_table = user_table_db.fetchall()

    conn.close()
    
    if user_table != []:
        return user_table
    else:
        return 'mot de passe ou identifiant incorrect'

def update_save_forapp(money, color, listValue, id):
    conn = sqlite3.connect('userdb.db')

    cur = conn.cursor()
    cur.execute("UPDATE User SET money=?, color=?, listValue=? WHERE id=?", (money, color, listValue, id))

    conn.commit()
    conn.close()