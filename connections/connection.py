import boto3
import os
from dotenv import load_dotenv
load_dotenv(dotenv_path = '../.env')
#import requests
from dotenv import load_dotenv
load_dotenv(dotenv_path = './.env')
from datetime import date
from boto3.dynamodb.conditions import Attr
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd



dynamo_client  =  boto3.resource(service_name = 'dynamodb',region_name = 'us-east-2',
              aws_access_key_id = os.environ.get('AWS_ACCESS_KEY_ID'),
              aws_secret_access_key = os.environ.get('AWS_SECRET_ACCESS_KEY'))

product_table = dynamo_client.Table('Trash_AI')
print(product_table.table_status) #should print ACTIVE if successfully connected

today = date.today()
today_string = today.strftime('%m/%d/%Y')


# product_table.put_item(Item = {'Type_of_Trash':'Paper',"Weight": 20,"Date": today_string})
# product_table.put_item(Item = {'Type_of_Trash':'Paper',"Weight": 30,"Date": today_string})
# product_table.put_item(Item = {'Type_of_Trash':'Plastic',"Weight": 20,"Date": today_string})
# product_table.put_item(Item = {'Type_of_Trash':'Plastic',"Weight": 30,"Date": today_string})
# product_table.put_item(Item = {'Type_of_Trash':'Regular Trash',"Weight": 20,"Date": today_string})
# product_table.put_item(Item = {'Type_of_Trash':'Regular Trash',"Weight": 30,"Date": today_string})
