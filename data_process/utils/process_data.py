import boto3
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('data-ingest')

def process_data(keys):
    print('process called')
    for key in keys[:1]:
        r = table.query(
            KeyConditionExpression=Key('address').eq(str(key[0])) & Key('inserted_at').eq(key[1])
        )
        print(r[u'Items'])
        integrate(r[u'Items'][0])
    return

def integrate(df):
    chunksize = 20
    total_area = []
    for i in range(0, len(df['x']), chunksize):
        x = df['x'][i:i+chunksize]
        y = df['y'][i:i+chunksize]
        z = df['z'][i:i+chunksize]
        area_x = simps(x)
        area_y = simps(y)
        area_z = simps(z)
        area = area_x + area_y + area_z
        total_area.append(abs(area))

    print(total_area)
    return total_area
