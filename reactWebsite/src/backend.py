from flask import Flask, request, jsonify
from flask_cors import CORS
import hashlib
import boto3
from boto3.dynamodb.conditions import Attr
import os
import requests
from dotenv import load_dotenv
load_dotenv(dotenv_path = '../.env')

#connection to aws dynamodb
dynamo_client  =  boto3.resource(service_name = 'dynamodb',region_name = 'us-east-2',
              aws_access_key_id = os.environ.get('AWS_ACCESS_KEY_ID'),
              aws_secret_access_key = os.environ.get('AWS_SECRET_ACCESS_KEY'))

User_Accounts_Table = dynamo_client.Table('User_Accounts')
print(User_Accounts_Table.table_status) #should print ACTIVE if successfully connected

#CREATING USER ACCOUNT
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
    #print(users[0])

    #adding the user information to the database
    User_Accounts_Table.put_item(Item = {'Username': name, 'email': email,'Password': password_hash})
    return jsonify({'message': 'User created successfully'})

@app.route('/login', methods=['POST'])
def login():
    email = request.json['email']
    password = request.json['password']

    # Hash the password
    password_hash = hashlib.sha256(password.encode()).hexdigest()

    print(email)
    print(password_hash)

    user_info = User_Accounts_Table.scan(Select = "ALL_ATTRIBUTES",
                  FilterExpression = Attr('email').eq(email) & Attr('Password').eq(password_hash))

    print(user_info['Items'])

    # print(len(user_info['Items']))
    # print(type(user_info['Items']))

    if len(user_info['Items']) == 0:
        return jsonify({'message': 'Login failed'})
        #redirect user to profiles page
    else:
        return jsonify({'message': 'Login successful'})
        #return user to login page

    # user_info = User_Accounts_Table.get_item(Key={'email': email, 'Password': password_hash})
    # print(user_info)
    
    # user_email = User_Accounts_Table.get_item(Key = {'email': email})
    # print(user_email['Item'])
    # user_password = User_Accounts_Table.get_item(Key = {'Password': password_hash})
    # print(user_password)
    
    #user = next((u for u in users if u['name'] == name and u['password_hash'] == password_hash), None)
    # if (username == name and user_password == password):
    #     return jsonify({'message': 'Login successful'})
    # else:
    #     return jsonify({'message': 'Login failed'})

# @app.route('/statistics', methods=['GET'])
# def get_statistics():
#     dynamo_client  =  boto3.resource(service_name = 'dynamodb',region_name = 'us-east-2',
#               aws_access_key_id = 'AKIAT5AFYW5OKABU7NV7',
#               aws_secret_access_key = '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')

#     Trash_Stats = dynamo_client.Table('trash_ai')
#     print(Trash_Stats.table_status) #should print ACTIVE if successfully connected
    
#     return jsonify({'test'})

    
if __name__ == '__main__':
    app.run()

