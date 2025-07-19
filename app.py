from flask import Flask, request, jsonify
from flask_cors import CORS
import uuid


app = Flask(__name__)
CORS(app)

users=[{'confirmPassword': 'maxadmin12354',
        'email': 'admin@gmail.com',
        'name': 'Max Essien', 'password': 'maxadmin12354',
        'userId': 'a23fd8fc-23d7-4295-b7e6-cea08c045077'}]

@app.route('/register', methods=["POST"])
def register():
    data = request.json
    user_id = str(uuid.uuid4())
    users.append({**data, 'userId': user_id})
    print(users)
    return jsonify({"message": "Received"}), 200

@app.route('/update', methods=["POST"])
def update():
    data = request.json
    for i in range(len(users)):
        if users[i]['userId']==data['userId']:
            users[i]=data
    print(users)
    return jsonify({"message": "Received"}), 200

@app.route('/login')
def login():
    print(users, 'login')
    return jsonify(users)

if __name__  == "__main__":
    app.run(debug=True)