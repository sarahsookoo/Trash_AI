import boto3
import os
from dotenv import load_dotenv
#load_dotenv(dotenv_path = '../.env')
#import requests
from dotenv import load_dotenv
load_dotenv(dotenv_path = '../reactWebsite/.env')
from datetime import date
from boto3.dynamodb.conditions import Attr
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

#hardcoded register ID: 7ecb75f8-738b-4e45-9a61-df1c5e6188c7

dynamo_client  =  boto3.resource(service_name = 'dynamodb',region_name = 'us-east-2',
              aws_access_key_id = os.environ.get('AWS_ACCESS_KEY_ID'),
              aws_secret_access_key = os.environ.get('AWS_SECRET_ACCESS_KEY'))

product_table = dynamo_client.Table('Trash_AI2')
print(product_table.table_status) #should print ACTIVE if successfully connected

user_data = product_table.scan(Select = "ALL_ATTRIBUTES",
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

print(Amount_of_Plastic)
print(Amount_of_Paper)
print(Amount_of_Trash)

for x in user_data['Items']:
    if x['payload']['Type_of_Trash'] == 'plastic':
        Weights_of_Plastic.append(x['payload']['Weight'])
    if x['payload']['Type_of_Trash'] == 'paper':
        Weights_of_Paper.append(x['payload']['Weight'])
    if x['payload']['Type_of_Trash'] == 'trash':
        Weights_of_Trash.append(x['payload']['Weight'])

print(Weights_of_Plastic)
print(Weights_of_Paper)
print(Weights_of_Trash)

for x in Weights_of_Plastic:
    Total_Weight_Plastic += x

for x in Weights_of_Paper:
    Total_Weight_Paper += x

for x in Weights_of_Trash:
    Total_Weight_Trash += x

print(Total_Weight_Plastic)
print(Total_Weight_Paper)
print(Total_Weight_Trash)

Avg_Weight_Plastic = Total_Weight_Plastic / Amount_of_Plastic
Avg_Weight_Paper = Total_Weight_Paper / Amount_of_Paper
Avg_Weight_Trash = Total_Weight_Trash / Amount_of_Trash

print(Avg_Weight_Plastic)
print(Avg_Weight_Paper)
print(Avg_Weight_Trash)

Types_of_Trash = ['Plastic', 'Paper', 'Regular Trash']
avg_weights = [Avg_Weight_Plastic, Avg_Weight_Paper, Avg_Weight_Trash]
df = pd.DataFrame({'Type of Trash': Types_of_Trash, 'Weight (grams)': avg_weights})

# Create bar plot
sns.set_style('whitegrid')
sns.barplot(x='Type of Trash', y='Weight (grams)', data=df)
plt.title('Average Weight of Trash')
plt.xlabel('Type of Trash')
plt.ylabel('Weight of Trash (grams)')
plt.show()






#print(user_data['Items'][0]
#{'registerID': '7ecb75f8-738b-4e45-9a61-df1c5e6188c7', 'payload': {'Type_of_Trash': 'plastic', 'Weight': Decimal('0')}, 'Timestamp': '05-14-2023-18:49:23'}

#print(user_data['Items'][0]['payload']['Type_of_Trash'])

#for all
#if register ID =  something 
#if type of trash from payload = paper
#add one to count
#add the weight
#find avg by dividing weight by count
#repeat for plastic and trash
