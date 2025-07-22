import sqlite3
import json

def create():

    connection = sqlite3.connect("users_results.db")
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users_results(
            user_id TEXT NOT NULL,
            course_code TEXT NOT NULL,
            score INTEGER NOT NULL,
            quiz_data TEXT NOT NULL,
            selected_answers TEXT NOT NULL,
            correct_answers TEXT NOT NULL,
            time_stamp TEXT
        )
    """)

    connection.commit()
    connection.close()

def add_new_result(user_id, course_code, score, quiz_data, selected_answers, correct_answers, time_stamp):
    connection = sqlite3.connect("users_results.db")
    cursor = connection.cursor()
    cursor.execute(
        "INSERT INTO users_results VALUES(?, ?, ?, ?, ?, ?, ?)",
        (user_id, course_code, score, quiz_data, selected_answers, correct_answers, time_stamp)
    )
    connection.commit()
    connection.close()

def remove_results_by_user(user_id):
    connection = sqlite3.connect("users_results.db")
    cursor = connection.cursor()
    cursor.execute(
        "DELETE FROM users_results WHERE user_id = (?)", (user_id,)
    )
    connection.commit()
    connection.close()

def fetch_results_by_user(id):
    connection = sqlite3.connect("users_results.db")
    cursor = connection.cursor()
    cursor.execute(
        "SELECT * FROM users_results WHERE user_id = (?)", (id,)
    )
    return cursor.fetchall()

def format_fetched_results(results_list):
    formatted_list = []
    if results_list:
        for result in results_list:
            formatted_list.append(
                {
                    "user_id": result[0],
                    "course_code": result[1],
                    "score": result[2],
                    "quiz_data": result[3],
                    "selected_answers": result[4],
                    "correct_answers": result[5],
                    "time_stamp": result[6]
                }
            )
    return formatted_list

def fetch_all_results():
    connection = sqlite3.connect("users_results.db")
    cursor = connection.cursor()
    cursor.execute(
        "SELECT * FROM users_results"
    )
    return cursor.fetchall()
    # print(cursor.fetchall())
    # connection.close()

def format_json_strings(json_list):
    tpp =[]
    for item in json_list:
        item = json.loads(item)
        # tpp.append(json.loads(item))
    print(tpp, 'yes')