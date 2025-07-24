import sqlite3
from datetime import datetime

def create_session_table():
    connection = sqlite3.connect("user_sessions.db")
    cursor = connection.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS user_sessions(
                    token TEXT NOT NULL UNIQUE,
                    user_id TEXT NOT NULL UNIQUE,
                    expiry_time INTERGER NOT NULL
                   )""")
    connection.commit()
    connection.close()

def fetch_all_sessions():
    connection = sqlite3.connect("user_sessions.db")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM user_sessions")
    result = cursor.fetchall()
    connection.close()
    return result

def add_session(token, user_id, expiry_time):
    connection = sqlite3.connect("user_sessions.db")
    cursor = connection.cursor()
    cursor.execute("DELETE FROM user_sessions")
    connection.commit()
    cursor.execute("INSERT INTO user_sessions VALUES (?, ?, ?)", (token, user_id, expiry_time))
    connection.commit()
    connection.close()

def fetch_user_with_token(token):
    connection = sqlite3.connect("user_sessions.db")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM user_sessions WHERE token = (?)", (token,))
    result = cursor.fetchone()
    connection.close()
    return result


def delete_session_with_token(token):
    connection = sqlite3.connect("user_sessions.db")
    cursor = connection.cursor()
    cursor.execute("DELETE FROM user_sessions WHERE token = (?)", (token,))
    connection.commit()
    connection.close()