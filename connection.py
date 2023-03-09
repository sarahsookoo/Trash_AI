import boto3
import os
#import requests

dynamo_client  =  boto3.resource(service_name = 'dynamodb',region_name = 'us-east-2',
              aws_access_key_id = '',
              aws_secret_access_key = '')

product_table = dynamo_client.Table('trash_ai')
product_table.table_status
