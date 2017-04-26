import boto3

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('data-ingest')

def process_data(keys):
    for key in keys:
        r = table.query(
            KeyConditionExpression=Key('address').eq(str(key[0])) & Key('inserted_at').eq(key[1])
        )
        print(r[u'Items'])
    return
