from datetime import datetime
import json


user_db = 'users.json'

def load_users():
    with open(user_db, 'r') as f:
        return json.load(f)

def save_users(user_data):
    with open(user_db, 'w') as f:
        json.dump(user_data, f, indent=4)

def current_time_stamp():
    return datetime.now().strftime('%D_%H:%M:%S')


account_data_db = "users-account-data.json"

def load_account_data():
    with open(account_data_db, 'r') as f:
        return json.load(f)

def update_data(new_account_data):
    with open(account_data_db, 'w') as f:
        return json.dump(new_account_data, f, indent=4)