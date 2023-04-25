import boto3
import os
#import requests
from dotenv import load_dotenv
load_dotenv(dotenv_path = './.env')

dynamo_client  =  boto3.resource(service_name = 'dynamodb',region_name = 'us-east-2',
              aws_access_key_id = os.environ.get('AWS_ACCESS_KEY_ID'),
              aws_secret_access_key = os.environ.get('AWS_SECRET_ACCESS_KEY'))

product_table = dynamo_client.Table('test')
print(product_table.table_status) #should print ACTIVE if successfully connected

product_table.put_item(Item = {'userID':1,"email":"test@test.com","Password":"testpassword"})
