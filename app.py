from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
import uuid
import json


app = Flask(__name__)
# CORS(app)
CORS(app, origins=[
    'https://maxquiz.netlify.app'
])

user_db = 'users.json'

def load_users():
    with open(user_db, 'r') as f:
        return json.load(f)

print(load_users())
def save_users(user_data):
    with open(user_db, 'w') as f:
        json.dump(user_data, f, indent=4)

print(datetime.now().strftime('%D_%H:%M:%S'))


# users=[{'confirmPassword': 'maxadmin12354',
#         'email': 'admin@gmail.com',
#         'name': 'Max Essien', 'password': 'maxadmin12354',
#         'userId': 'a23fd8fc-23d7-4295-b7e6-cea08c045077'}]
@app.route('/download-data')
def download_data():
    user_dict = load_users()
    date = datetime.now().strftime('%D_%H:%M:%S')
    user_dict[0]={"date": date}
    return jsonify(user_dict)


@app.route('/register', methods=["POST"])
def register():
    data = request.json
    users_dict = load_users()
    print(data)
    for i in range(1, len(users_dict)):
        if users_dict[i]["email"]==data["email"]:
            return jsonify(True)
    user_id = str(uuid.uuid4())
    data_with_id = {**data, 'userId': user_id}
    user_dict = load_users()
    user_dict.append(data_with_id)
    save_users(user_dict)
    print(user_dict)
    return jsonify(False)

@app.route('/update', methods=["POST"])
def update():
    data = request.json
    users_dict = load_users()
    for i in range(1, len(users_dict)):
        if users_dict[i]['userId']==data['userId']:
            users_dict[i]=data
    save_users(users_dict)
    return jsonify({"message": "Account update successful"}), 200

@app.route('/login', methods=["POST"])
def login():
    data = request.json
    users_dict = load_users()
    for i in range(1, len(users_dict)):
        if users_dict[i]["email"]==data["email"] and users_dict[i]["password"]==data["password"]:
            print(users_dict[i], 'login')
            user=True
            return jsonify(users_dict[i])
        else:
            user=False
    if not user:
        return jsonify(False)

account_data_db = "users-account-data.json"

def load_account_data():
    with open(account_data_db, 'r') as f:
        return json.load(f)

def update_data(new_account_data):
    with open(account_data_db, 'w') as f:
        return json.dump(new_account_data, f, indent=4)

@app.route('/update_account_data', methods=['POST'])
def update_account_data():
    data = request.json
    account_data = load_account_data()
    found = False
    for i in range(len(account_data)):
        if account_data[i]['userId']==data['userId']:
            account_data[i]=data
            found = True
            update_data(account_data)
            return jsonify(account_data[i])
    if not found:
        account_data.append(data)
    update_data(account_data)
    return jsonify(account_data)

@app.route('/account_data', methods=['POST'])
def account_data():
    data = request.json
    account_data = load_account_data()
    found=False
    for i in range(len(account_data)):
        if account_data[i]["userId"]==data["userId"]:
            found=True
            return jsonify(account_data[i])
    if not found:
        account_data.append({
            "quizzesTaken": [],
            "userId": data["userId"]
        })
    update_data(account_data)
    return jsonify(account_data)


if __name__  == "__main__":
    app.run(debug=True)