from flask import Flask, request, jsonify
from flask_cors import CORS
import hashlib

app = Flask(__name__)
CORS(app, origins="*")

users = []

@app.route('/signup', methods=['POST'])
def signup():
    name = request.json['name']
    email = request.json['email']
    password = request.json['password']
    
    # Hash the password
    password_hash = hashlib.sha256(password.encode()).hexdigest() 
    
    user = {'name': name, 'email': email, 'password_hash': password_hash}
    users.append(user)
    print(users[0])
    return jsonify({'message': 'User created successfully'})

@app.route('/login', methods=['POST'])
def login():
    email = request.json['email']
    password = request.json['password']

    # Hash the password
    password_hash = hashlib.sha256(password.encode()).hexdigest()

    user = next((u for u in users if u['email'] == email and u['password_hash'] == password_hash), None)
    if user:
        return jsonify({'message': 'Login successful'})
    else:
        return jsonify({'message': 'Login failed'})
    
if __name__ == '__main__':
    app.run()

#print(product_table.table_status)