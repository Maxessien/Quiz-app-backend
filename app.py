from flask import Flask, request, jsonify, session
from flask_cors import CORS
import uuid
import json
from utils.utils import load_users, current_time_stamp
from utils.users_utils import add_user, update_user, fetch_all, fetch_user_by_email, delete_user, format_user_tuple, fetch_by_email_and_password
from utils.user_results_data import create, add_new_result, format_json_strings, remove_results_by_user, fetch_all_results, fetch_results_by_user, format_fetched_results


app = Flask(__name__)
# CORS(app)
CORS(app, origins=[
    'https://maxquiz.netlify.app'
])


# fetch_all()

# delete_user("6ffee068-4c55-4729-95c5-45a9aa8d185d")
# fetch_all()

create()

# fetch_all_results()


@app.route('/download-data')
def download_data():
    return jsonify(fetch_all_results())

@app.route('/download-data-users')
def download_data():
    return jsonify(fetch_all())


@app.route('/register', methods=["POST"])
def register():
    data = request.json
    user_exists = fetch_user_by_email(data["email"])
    if not user_exists:
        new_id = str(uuid.uuid4())
        add_user(data["name"], data["email"], data["password"], new_id)
        fetch_all()
        return jsonify({"success": True, "message": "Account successfully created"})
    else:
        fetch_all()
        return jsonify({"success": False, "message": "User already exists"})
    


@app.route('/update', methods=["POST"])
def update():
    data = request.json
    update_user(data["name"], data["email"], data["password"], data["userId"])
    return jsonify({"message": "Account update successful"}), 200




@app.route('/login', methods=["POST"])
def login():
    data = request.json
    user_exists = fetch_by_email_and_password(data["email"], data["password"])
    if not user_exists:
        print(user_exists)
        return jsonify(False)
    else:
        print(user_exists)
        return format_user_tuple(user_exists[0])



@app.route('/update_results_db', methods=['POST'])
def update_results_db():
    data = request.json
    json_quiz_data = json.dumps(data["quiz_data"])
    json_selected_answers = json.dumps(data["selected_answers"])
    json_correct_answers = json.dumps(data["correct_answers"])
    print(json_quiz_data)
    add_new_result(data["user_id"], data["course_code"], data["score"], json_quiz_data, 
                    json_selected_answers, json_correct_answers, data["time_stamp"])
    return jsonify({"success": True, "message": "update successful"})
    

@app.route('/results_data/<string:user_id>')
def results_data(user_id):
    print(user_id, "iddd")
    results = fetch_results_by_user(user_id)
    result_dict = format_fetched_results(results)
    return jsonify(result_dict)


if __name__  == "__main__":
    app.run(debug=True)