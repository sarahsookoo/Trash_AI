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
    
        Trash_Stats = dynamo_client.Table('Trash_AI')
        
        #print(Trash_Stats.table_status) #should print ACTIVE if successfully connected

        ### PAPER DATA ###

        paper_data = Trash_Stats.scan(Select = "ALL_ATTRIBUTES",
                    FilterExpression = Attr('Type_of_Trash').eq('Paper'))

        Paper_Items = paper_data['Items'] #all attributes that are paper
        Amount_of_Paper = len(Paper_Items) #amount of attributes

        Paper_Weights = 0

        for x in Paper_Items:
            Paper_Weights += x['Weight'] #add up the weight of all paper items

        Paper_Avg_Weight = Paper_Weights/Amount_of_Paper #divide total weight by amount of paper items for average
        #print(Paper_Avg_Weight) #should be 25
        
        ### PLASTIC DATA ###
        plastic_data = Trash_Stats.scan(Select = "ALL_ATTRIBUTES",
                FilterExpression = Attr('Type_of_Trash').eq('Plastic'))

        Plastic_Items = plastic_data['Items'] #all attributes that are plastic
        Amount_of_Plastic = len(Plastic_Items) #amount of attributes

        Plastic_Weights = 0

        for x in Plastic_Items:
            Plastic_Weights += x['Weight'] #add up the weight of all plastic items

        Plastic_Avg_Weight = Plastic_Weights/Amount_of_Plastic #divide total weight by amount of plastic items for average
        #print(Plastic_Avg_Weight) #should be 25

        ### REGULAR TRASH DATA ###
        regular_trash_data = Trash_Stats.scan(Select = "ALL_ATTRIBUTES",
                FilterExpression = Attr('Type_of_Trash').eq('trash'))

        Regular_Trash_Items = regular_trash_data['Items'] #all attributes that are trash
        Amount_of_Regular_Trash = len(Regular_Trash_Items) #amount of attributes

        Regular_Trash_Weights = 0

        for x in Regular_Trash_Items:
            Regular_Trash_Weights += x['Weight'] #add up the weight of all trash items

        Regular_Trash_Avg_Weight = Regular_Trash_Weights/Amount_of_Regular_Trash #divide total weight by amount of trash items for average
        #print(Regular_Trash_Avg_Weight) #should be 25

        Types_of_Trash = ['Paper', 'Plastic', 'Regular Trash']
        avg_weights = [Paper_Avg_Weight, Plastic_Avg_Weight, Regular_Trash_Avg_Weight]
        df = pd.DataFrame({'Type of Trash': Types_of_Trash, 'Weight (grams)': avg_weights})

        # Create bar plot
        sns.set_style('whitegrid')
        sns.barplot(x='Type of Trash', y='Weight (grams)', data=df)
        plt.title('Average Weight of Trash')
        plt.xlabel('Type of Trash')
        plt.ylabel('Weight of Trash (grams)')
        #plt.show()
        plot_path = './src/components/pages/avgs.jpg'  # Change this to a valid path
        plt.savefig(plot_path)

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
#                 aws_access_key_id = os.environ.get('AWS_ACCESS_KEY_ID'),
#                 aws_secret_access_key = os.environ.get('AWS_SECRET_ACCESS_KEY'))
    
#     Trash_Stats = dynamo_client.Table('Trash_AI')
    
#     #print(Trash_Stats.table_status) #should print ACTIVE if successfully connected

#     ### PAPER DATA ###

#     paper_data = Trash_Stats.scan(Select = "ALL_ATTRIBUTES",
#                 FilterExpression = Attr('Type_of_Trash').eq('Paper'))

#     Paper_Items = paper_data['Items'] #all attributes that are paper
#     Amount_of_Paper = len(Paper_Items) #amount of attributes

#     Paper_Weights = 0

#     for x in Paper_Items:
#         Paper_Weights += x['Weight'] #add up the weight of all paper items

#     Paper_Avg_Weight = Paper_Weights/Amount_of_Paper #divide total weight by amount of paper items for average
#     #print(Paper_Avg_Weight) #should be 25
    
#     ### PLASTIC DATA ###
#     plastic_data = Trash_Stats.scan(Select = "ALL_ATTRIBUTES",
#             FilterExpression = Attr('Type_of_Trash').eq('Plastic'))

#     Plastic_Items = plastic_data['Items'] #all attributes that are plastic
#     Amount_of_Plastic = len(Plastic_Items) #amount of attributes

#     Plastic_Weights = 0

#     for x in Plastic_Items:
#         Plastic_Weights += x['Weight'] #add up the weight of all plastic items

#     Plastic_Avg_Weight = Plastic_Weights/Amount_of_Plastic #divide total weight by amount of plastic items for average
#     #print(Plastic_Avg_Weight) #should be 25

#     ### REGULAR TRASH DATA ###
#     regular_trash_data = Trash_Stats.scan(Select = "ALL_ATTRIBUTES",
#             FilterExpression = Attr('Type_of_Trash').eq('trash'))

#     Regular_Trash_Items = regular_trash_data['Items'] #all attributes that are trash
#     Amount_of_Regular_Trash = len(Regular_Trash_Items) #amount of attributes

#     Regular_Trash_Weights = 0

#     for x in Regular_Trash_Items:
#         Regular_Trash_Weights += x['Weight'] #add up the weight of all trash items

#     Regular_Trash_Avg_Weight = Regular_Trash_Weights/Amount_of_Regular_Trash #divide total weight by amount of trash items for average
#     #print(Regular_Trash_Avg_Weight) #should be 25

#     Types_of_Trash = ['Paper', 'Plastic', 'Regular Trash']
#     avg_weights = [Paper_Avg_Weight, Plastic_Avg_Weight, Regular_Trash_Avg_Weight]
#     df = pd.DataFrame({'Type of Trash': Types_of_Trash, 'Weight (grams)': avg_weights})

#     # Create bar plot
#     sns.set_style('whitegrid')
#     sns.barplot(x='Type of Trash', y='Weight (grams)', data=df)
#     plt.title('Average Weight of Trash')
#     plt.xlabel('Type of Trash')
#     plt.ylabel('Weight of Trash (grams)')
#     #plt.show()
#     plot_path = './avgs.png'  # Change this to a valid path
#     plt.savefig(plot_path)
#     # plot_path_profile = '../avgs.png'
    
#     return jsonify({'plot_path': plot_path})


if __name__ == '__main__':
    app.run()

