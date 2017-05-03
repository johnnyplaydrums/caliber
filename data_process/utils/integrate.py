import boto3, decimal
import numpy as np
from datetime import datetime
from boto3.dynamodb.conditions import Key
from scipy.integrate import simps


dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
data_ingest_table = dynamodb.Table('data-ingest')
data_process_table = dynamodb.Table('data-process')


def integrate(df, address):
    chunksize = 40
    total_area = []
    xa = np.array(df['x']).astype(float)
    ya = np.array(df['y']).astype(float)
    za = np.array(df['z']).astype(float)
    for i in range(0, len(df['x']), chunksize):
        x = xa[i:i+chunksize]
        y = ya[i:i+chunksize]
        z = za[i:i+chunksize]
        area_x = simps(x)
        area_y = simps(y)
        area_z = simps(z)
        area = area_x + area_z
        total_area.append(area)

    total_area = str(round(np.mean(total_area), 15))

    address_item = data_process_table.get_item(
        Key= {
            'address': address
        }
    )

    if u'Item' in address_item:
        item = address_item[u'Item']
        old_mean = decimal.Decimal(item[u'mean'])
        mean_count = item[u'mean_count']
        new_mean = str(round(((mean_count * old_mean) + decimal.Decimal(total_area)) / (mean_count + 1), 15))
        print('Update address: %s' % address, old_mean, new_mean, total_area)
        r = data_process_table.update_item(
            Key={
                'address': address
            },
            UpdateExpression="set mean_count = mean_count + :c, mean = :m",
            ExpressionAttributeValues={
                ':c': decimal.Decimal(1),
                ':m': new_mean
            },
        )
    else:
        print('New address: %s' % address, total_area)
        inserted_at = datetime.now().strftime('%Y%m%d%H%M%S%f')
        item = {
            'address': address,
            'mean': total_area,
            'mean_count': decimal.Decimal(1),
            'inserted_at': inserted_at,
            'start_lat': df['start_lat'],
            'start_long': df['start_long'],
            'end_lat': df['end_lat'],
            'end_long': df['end_long']
        }
        data_process_table.put_item(Item=item)


    return total_area
