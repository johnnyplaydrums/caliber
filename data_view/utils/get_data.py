import boto3
from datetime import datetime
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
data_process_table = dynamodb.Table('data-process-test')


def get_recent():
    addresses = get_all()
    sorted_addresses = sorted(addresses,
                              key=lambda address: int(address['updated_at']),
                              reverse=True)[:15]
    sorted_addresses = update_addresses(sorted_addresses)
    return sorted_addresses


def get_worst():
    addresses = get_all()
    sorted_addresses = sorted(addresses,
                              key=lambda address: float(address['mean']),
                              reverse=True)[:15]
    sorted_addresses = update_addresses(sorted_addresses)
    return sorted_addresses


def get_all():
    response = data_process_table.scan()
    addresses = response['Items']
    while 'LastEvaluatedKey' in response:
        response = data_process_table.scan(
            ExclusiveStartKey=response['LastEvaluatedKey']
        )
        addresses.extend(response['Items'])
    return addresses

def update_addresses(addresses):
    for address in addresses:
        time = datetime.strptime(str(address['updated_at']), '%Y%m%d%H%M%S%f')
        address['updated_at'] = datetime.strftime(time, '%b %d %Y %I:%M:%S %p')
        address['mean_count'] = int(address['mean_count'])
        address['address'] = ','.join(address['address'].split(',', 2)[:2])

    return addresses
