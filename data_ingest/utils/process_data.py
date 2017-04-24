import boto3, geocoder, math
from datetime import datetime

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('data-ingest')

def send_to_dynamodb(data):
    for item in data:
        table.put_item(Item=data[item])
    return


def process_data(data):
    address_points = {}
    last_point = (0,0)

    for index in range(len(data['lat'])):
        current_point = (data['lat'][index], data['long'][index])
        if last_point != current_point:
            print(last_point, current_point)
            address = geocoder.google([current_point[0], current_point[1]], method='reverse')
            last_address = str(int(math.ceil(int(address.address.split(' ', 1)[0]) / 100) * 100)) + ' ' + address.address.split(' ', 1)[1]
            if last_address in address_points:
                address_points[last_address]['lat'].append(current_point[0])
                address_points[last_address]['long'].append(current_point[1])
                address_points[last_address]['x'].append(data['x'][index])
                address_points[last_address]['y'].append(data['y'][index])
                address_points[last_address]['z'].append(data['z'][index])
            else:
                address_points[last_address] = {
                    'lat': [current_point[0]],
                    'long': [current_point[1]],
                    'x': [data['x'][index]],
                    'y': [data['y'][index]],
                    'z': [data['z'][index]],
                    'inserted_at': datetime.now().strftime('%Y%m%d%H%M%S%f'),
                    'address': last_address,
                    'processed': 'false'
                }

            last_point = current_point
            print(last_address)
        else:
            address_points[last_address]['lat'].append(current_point[0])
            address_points[last_address]['long'].append(current_point[1])
            address_points[last_address]['x'].append(data['x'][index])
            address_points[last_address]['y'].append(data['y'][index])
            address_points[last_address]['z'].append(data['z'][index])

    send_to_dynamodb(address_points)
    return
