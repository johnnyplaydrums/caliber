import boto3, geocoder, math, re
from datetime import datetime
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('data-ingest')

def send_to_dynamodb(data):
    for item in data:
        table.put_item(Item=data[item])
    return


def process_data(data):
    address_points = {}
    keys = []
    last_point = (0,0)

    for index in range(len(data['lat'])):
        current_point = (data['lat'][index], data['long'][index])
        if last_point != current_point:
            address = geocoder.google([current_point[0], current_point[1]], method='reverse')
            address_range = re.search(r'(\d)+-', address.address)

            if address.housenumber == None:
                print('NO HOUSE NUMBER')
            if address_range != None:
                print('SPLIT ADDRESS:')
                print(address.address)
                address = address.address.split('-', 1)[0] + ' ' + address.address.split(' ', 1)[1]
                prev = last_address
                last_address = str(int(math.ceil(int(address.split(' ', 1)[0]) / 100) * 100)) + ' ' + address.split(' ', 1)[1]
            else:
                prev = last_address
                last_address = str(int(math.ceil(int(address.address.split(' ', 1)[0]) / 100) * 100)) + ' ' + address.address.split(' ', 1)[1]

            if last_address in address_points:
                address_points[last_address]['lat'].append(current_point[0])
                address_points[last_address]['long'].append(current_point[1])
                address_points[last_address]['x'].append(data['x'][index])
                address_points[last_address]['y'].append(data['y'][index])
                address_points[last_address]['z'].append(data['z'][index])
            else:
                print('Adding data to', last_address)
                inserted_at = datetime.now().strftime('%Y%m%d%H%M%S%f')
                address_points[prev] = {
                    'end_lat': data['lat'][index - 1],
                    'end_long': data['long'][index - 1]
                }
                address_points[last_address] = {
                    'start_lat': current_point[0],
                    'start_long': current_point[1],
                    'lat': [current_point[0]],
                    'long': [current_point[1]],
                    'x': [data['x'][index]],
                    'y': [data['y'][index]],
                    'z': [data['z'][index]],
                    'inserted_at': inserted_at,
                    'address': last_address,
                    'processed': 'false'
                }
                keys.append((last_address, inserted_at))

            last_point = current_point
        else:
            address_points[last_address]['lat'].append(current_point[0])
            address_points[last_address]['long'].append(current_point[1])
            address_points[last_address]['x'].append(data['x'][index])
            address_points[last_address]['y'].append(data['y'][index])
            address_points[last_address]['z'].append(data['z'][index])

    send_to_dynamodb(address_points)
    return keys
