import boto3
from datetime import datetime
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
data_process_table = dynamodb.Table('data-process')


def get_recent():
    addresses = get_all()
    sorted_addresses = sorted(addresses,
                              key=lambda address: int(address['updated_at']),
                              reverse=True)[:20]

    for address in sorted_addresses:
        time = datetime.strptime(str(address['updated_at']), '%Y%m%d%H%M%S%f')
        address['updated_at'] = datetime.strftime(time, '%b %d %Y %I:%M:%S %p')
    return sorted_addresses


def get_worst():
    addresses = get_all()
    sorted_addresses = sorted(addresses,
                              key=lambda address: float(address['mean']),
                              reverse=True)[:20]

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
