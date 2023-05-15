from flask import Flask, request, jsonify
from flask_cors import CORS
import hashlib
import boto3
from boto3.dynamodb.conditions import Attr
import os
import requests
from dotenv import load_dotenv
load_dotenv(dotenv_path = '../.env')
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

#Establish connection to AWS DynamoDB and create resource for User_Accounts table
dynamo_client  =  boto3.resource(service_name = 'dynamodb',region_name = 'us-east-2',
                aws_access_key_id = os.environ.get('AWS_ACCESS_KEY_ID'),
                aws_secret_access_key = os.environ.get('AWS_SECRET_ACCESS_KEY'))

User_Accounts_Table = dynamo_client.Table('User_Accounts')
print(User_Accounts_Table.table_status) #should print ACTIVE if successfully connected

#CREATING USER ACCOUNT
#Create a flask app and set up CORS to allow cross origin resource sharing
app = Flask(__name__)
CORS(app, origins="*")

users = []

#This called when the user signs up by submitting the sign up form
#It extracts the user's name, email, and password
#The password is hashed using the SHA256 algorithm
#The user info is added to the user list and to the DynamoDB table
#returns a success message
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

#This function is called when the user presses submit on the login form
#It takes the user input and before checking the db, it uses the SHA256 algorithm to has the password
#The function queries the table for matching records and if found, there is a success message
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

        dynamo_client  =  boto3.resource(service_name = 'dynamodb',region_name = 'us-east-2',
                aws_access_key_id = os.environ.get('AWS_ACCESS_KEY_ID'),
                aws_secret_access_key = os.environ.get('AWS_SECRET_ACCESS_KEY'))

    
        Trash_Stats = dynamo_client.Table('Trash_AI2')
        user_data = Trash_Stats.scan(Select = "ALL_ATTRIBUTES",
                    FilterExpression = Attr('registerID').eq('7ecb75f8-738b-4e45-9a61-df1c5e6188c7'))

        Amount_of_Plastic = 0
        Amount_of_Paper = 0
        Amount_of_Trash = 0

        types_of_trash = []

        Weights_of_Plastic = []
        Weights_of_Paper = []
        Weights_of_Trash = []

        Total_Weight_Plastic = 0
        Total_Weight_Paper = 0
        Total_Weight_Trash = 0

        for x in user_data['Items']:
            types_of_trash.append(x['payload']['Type_of_Trash'])

        #print(types_of_trash)
        for x in types_of_trash:
            if x == 'plastic':
                Amount_of_Plastic += 1
            elif x == 'paper':
                Amount_of_Paper += 1
            else:
                Amount_of_Trash += 1

        # print(Amount_of_Plastic)
        # print(Amount_of_Paper)
        # print(Amount_of_Trash)

        for x in user_data['Items']:
            if x['payload']['Type_of_Trash'] == 'plastic':
                Weights_of_Plastic.append(x['payload']['Weight'])
            if x['payload']['Type_of_Trash'] == 'paper':
                Weights_of_Paper.append(x['payload']['Weight'])
            if x['payload']['Type_of_Trash'] == 'trash':
                Weights_of_Trash.append(x['payload']['Weight'])

        # print(Weights_of_Plastic)
        # print(Weights_of_Paper)
        # print(Weights_of_Trash)

        for x in Weights_of_Plastic:
            Total_Weight_Plastic += x

        for x in Weights_of_Paper:
            Total_Weight_Paper += x

        for x in Weights_of_Trash:
            Total_Weight_Trash += x

        # print(Total_Weight_Plastic)
        # print(Total_Weight_Paper)
        # print(Total_Weight_Trash)

        Avg_Weight_Plastic = Total_Weight_Plastic / Amount_of_Plastic
        Avg_Weight_Paper = Total_Weight_Paper / Amount_of_Paper
        Avg_Weight_Trash = Total_Weight_Trash / Amount_of_Trash

        # print(Avg_Weight_Plastic)
        # print(Avg_Weight_Paper)
        # print(Avg_Weight_Trash)

        Types_of_Trash = ['Plastic', 'Paper', 'Regular Trash']
        avg_weights = [Avg_Weight_Plastic, Avg_Weight_Paper, Avg_Weight_Trash]
        df = pd.DataFrame({'Type of Trash': Types_of_Trash, 'Weight (grams)': avg_weights})

        # Create bar plot
        sns.set_style('whitegrid')
        sns.barplot(x='Type of Trash', y='Weight (grams)', data=df)
        plt.title('Average Weight of Trash')
        plt.xlabel('Type of Trash')
        plt.ylabel('Weight of Trash (grams)')
        #plt.show()
        plot_path = './components/pages/avgs.jpg'  # Change this to a valid path
        plt.savefig(plot_path)

        # Types_of_Trash = ['Plastic', 'Paper', 'Regular Trash']
        # amt_trash = [Amount_of_Plastic, Amount_of_Paper, Amount_of_Trash]
        # df = pd.DataFrame({'Type of Trash': Types_of_Trash, 'Amount of Items': amt_trash})

        # # Create bar plot
        # sns.set_style('whitegrid')
        # sns.barplot(x='Type of Trash', y='Amount of Items', data=df)
        # plt.title('Amount of Items per Each Class of Trash')
        # plt.xlabel('Type of Trash')
        # plt.ylabel('Amount of Items')
        # #plt.show()
        # plot_path = './components/pages/amt.jpg'  # Change this to a valid path
        # plt.savefig(plot_path)
        
        return jsonify({'message': 'Login successful'})
        #return user to login page

if __name__ == '__main__':
    app.run()
