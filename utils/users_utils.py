import sqlite3

connection = sqlite3.connect('users.db')
cursor = connection.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS users(
               name TEXT NOT NULL,
               email TEXT NOT NULL UNIQUE,
               password TEXT NOT NULL,
               user_id TEXT NOT NULL UNIQUE
    )
""")

connection.commit()
connection.close()

def add_user(name, email, password, id):
    connection = sqlite3.connect('users.db')
    cursor = connection.cursor()
    cursor.execute("INSERT INTO users VALUES(?, ?, ?, ?)",
                    (name, email, password, id))
    connection.commit()
    cursor.execute("SELECT * FROM users")

def update_user(name, email, password, id):
    connection = sqlite3.connect('users.db')
    cursor = connection.cursor()
    cursor.execute("UPDATE users SET name=?, email=?, password=? WHERE user_id=?",
                    (name, email, password, id))
    connection.commit()
    connection.close()

def fetch_all():
    connection = sqlite3.connect('users.db')
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users")
    return cursor.fetchall()
    # print(cursor.fetchall())

def fetch_user_by_email(email):
    connection = sqlite3.connect('users.db')
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users WHERE email = (?)", (email,))
    return cursor.fetchall()

def fetch_user_by_id(id):
    connection = sqlite3.connect('users.db')
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users WHERE user_id = (?)", (id,))
    return cursor.fetchone()

def fetch_by_email_and_password(email, password):
    connection = sqlite3.connect('users.db')
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users WHERE email = (?) and password = (?)", (email, password))
    return cursor.fetchone()

def delete_user(id):
    print(id)
    connection = sqlite3.connect('users.db')
    cursor = connection.cursor()
    cursor.execute("DELETE FROM users WHERE user_id = (?)", (id,))
    connection.commit()
    connection.close()

def format_user_tuple(user_tuple, token):
    if user_tuple:
        user_dict = {
            "name": user_tuple[0],
            "email": user_tuple[1],
            "password": user_tuple[2],
            "userId": user_tuple[3],
            "sessionToken": token
        }
        return user_dict