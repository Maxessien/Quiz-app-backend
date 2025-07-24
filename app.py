from flask import Flask, request, jsonify, session
from flask_cors import CORS
from datetime import datetime
import uuid
import json
from utils.utils import load_users, current_time_stamp
from utils.users_utils import add_user, update_user, fetch_all, fetch_user_by_email, delete_user, format_user_tuple, fetch_by_email_and_password, fetch_user_by_id
from utils.user_results_data import create, add_new_result, format_json_strings, remove_results_by_user, fetch_all_results, fetch_results_by_user, format_fetched_results
from utils.user_session import fetch_user_with_token, delete_session_with_token, add_session, fetch_all_sessions, create_session_table

app = Flask(__name__)
# CORS(app)
CORS(app, origins=[
    'https://maxquiz.netlify.app'
])

print(int(datetime.now().timestamp()*1000))

# fetch_all()

# delete_user("6ffee068-4c55-4729-95c5-45a9aa8d185d")
# fetch_all()

create()
create_session_table()

# fetch_all_results()


@app.route('/download-data')
def download_data():
    return jsonify(fetch_all_results())

@app.route('/download-data-users')
def download_data_users():
    return jsonify(fetch_all())


@app.route('/register', methods=["POST"])
def register():
    data = request.json
    user_exists = fetch_user_by_email(data["email"])
    if not user_exists:
        new_id = str(uuid.uuid4())
        add_user(data["name"], data["email"], data["password"], new_id)
        return jsonify({"success": True, "message": "Account successfully created"}), 201
    else:
        fetch_all()
        return jsonify({"success": False, "message": "User already exists"})
    


@app.route('/update', methods=["POST"])
def update():
    data = request.json
    update_user(data["name"], data["email"], data["password"], data["userId"])
    return '', 204




@app.route('/login', methods=["POST"])
def login():
    data = request.json
    token = str(uuid.uuid4())
    expiry_time = (int(datetime.now().timestamp()*1000)) + (60*60*1000)
    user_exists = fetch_by_email_and_password(data["email"], data["password"])
    if not user_exists:
        print(user_exists)
        return ''
    else:
        add_session(token, user_exists[3], expiry_time)
        print(fetch_all_sessions())
        print(user_exists)
        return jsonify(format_user_tuple(user_exists, token))
    
@app.route("/login_with_token/<string:token>")
def login_with_token(token):
    user = fetch_user_with_token(token)
    current_time = int(datetime.now().timestamp()*1000)
    print(user, current_time)
    if user:
        if user[2] < current_time:
            print("deleted", user[2], current_time)
            delete_session_with_token(user[0])
            return '', 401
        else:
            logged_user = fetch_user_by_id(user[1])
            print("not deleted", format_user_tuple(logged_user, token))
            return jsonify(format_user_tuple(logged_user, token))
    else:
        return '', 401

@app.route("/delete_with_token/<string:token>", methods=['POST'])
def delete_with_token(token):
    print(token)
    delete_session_with_token(token)
    return ({"message": "successful"}), 200


    




@app.route('/update_results_db', methods=['POST'])
def update_results_db():
    data = request.json
    json_quiz_data = json.dumps(data["quiz_data"])
    json_selected_answers = json.dumps(data["selected_answers"])
    json_correct_answers = json.dumps(data["correct_answers"])
    add_new_result(data["user_id"], data["course_code"], data["score"], json_quiz_data, 
                    json_selected_answers, json_correct_answers, data["time_stamp"])
    return '', 204


@app.route('/reset_results_data', methods=['POST'])
def reset_results_data():
    data = request.json
    user_result = fetch_results_by_user(data['user_id'])
    if user_result:
        remove_results_by_user(data['user_id'])
    return '', 204

@app.route('/results_data/<string:user_id>')
def results_data(user_id):
    print(user_id, "iddd")
    results = fetch_results_by_user(user_id)
    result_dict = format_fetched_results(results)
    return jsonify(result_dict)


if __name__  == "__main__":
    app.run(debug=True)