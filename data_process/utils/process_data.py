import boto3, decimal
import numpy as np
from boto3.dynamodb.conditions import Key
from scipy.integrate import simps
from integrate import integrate
from update_ratings import update_ratings


dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
data_ingest_table = dynamodb.Table('data-ingest')
data_process_table = dynamodb.Table('data-process')

def process_data(keys):
    for key in keys:
        r = data_ingest_table.query(
            KeyConditionExpression=Key('address').eq(str(key[0])) & Key('inserted_at').eq(key[1])
        )
        integrate(r[u'Items'], key[0])

    ratings = update_ratings()
    print('Rated streets:')
    print(ratings)
    return
