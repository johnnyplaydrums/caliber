import boto3
from datetime import datetime
import decimal

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('data-ingest')

def send_to_dynamodb(data):
    for item in data:
        table.put_item(
            Item=data[item]
        )
    return
