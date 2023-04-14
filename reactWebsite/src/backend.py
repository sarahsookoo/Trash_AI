from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

users = []

@app.route('/signup', methods=['POST'])
def signup():
    name = request.json['name']
    email = request.json['email']
    password = request.json['password']
    user = {'name': name, 'email': email, 'password': password}
    users.append(user)
    return jsonify({'message': 'User created successfully'})

@app.route('/login', methods=['POST'])
def login():
    email = request.json['email']
    password = request.json['password']
    user = next((u for u in users if u['email'] == email and u['password'] == password), None)
    if user:
        return jsonify({'message': 'Login successful'})
    else:
        return jsonify({'message': 'Login failed'})
    
if __name__ == '__main__':
    app.run()
