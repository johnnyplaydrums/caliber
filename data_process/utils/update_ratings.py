import boto3, decimal
import numpy as np
from datetime import datetime
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
data_ingest_table = dynamodb.Table('data-ingest')
data_process_table = dynamodb.Table('data-process')

def update_ratings():
    # retrieve all streets
    response = data_process_table.scan()
    addresses = response['Items']

    # if we havent recieve all streets yet, continue collecting the rest
    while 'LastEvaluatedKey' in response:
        print('Getting more!')
        response = data_process_table.scan(
            ExclusiveStartKey=response['LastEvaluatedKey']
        )
        addresses.extend(response['Items'])

    # jenks breaks algorithm
    rated_streets = classify(addresses)

    # update streets with new score
    for address in rated_streets:
        updated_at = datetime.now().strftime('%Y%m%d%H%M%S%f')
        response = data_process_table.update_item(
            Key={
                'address': address['address']
            },
            UpdateExpression="set rating = :r",
            ExpressionAttributeValues={
                ':r': address['rating']
            }
        )
    return rated_streets


def get_jenks_breaks(data_list, number_class):
    data_list.sort()
    mat1 = []
    for i in range(len(data_list) + 1):
        temp = []
        for j in range(number_class + 1):
            temp.append(0)
        mat1.append(temp)
    mat2 = []
    for i in range(len(data_list) + 1):
        temp = []
        for j in range(number_class + 1):
            temp.append(0)
        mat2.append(temp)
    for i in range(1, number_class + 1):
        mat1[1][i] = 1
        mat2[1][i] = 0
        for j in range(2, len(data_list) + 1):
            mat2[j][i] = float('inf')
    v = 0.0
    for l in range(2, len(data_list) + 1):
        s1 = 0.0
        s2 = 0.0
        w = 0.0
        for m in range(1, l + 1):
            i3 = l - m + 1
            val = float(data_list[i3 - 1])
            s2 += val * val
            s1 += val
            w += 1
            v = s2 - (s1 * s1) / w
            i4 = i3 - 1
            if i4 != 0:
                for j in range(2, number_class + 1):
                    if mat2[l][j] >= (v + mat2[i4][j - 1]):
                        mat1[l][j] = i3
                        mat2[l][j] = v + mat2[i4][j - 1]
        mat1[l][1] = 1
        mat2[l][1] = v
    k = len(data_list)
    kclass = []
    for i in range(number_class + 1):
        kclass.append(float(min(data_list)))
    kclass[number_class] = float(data_list[len(data_list) - 1])
    count_num = number_class
    while count_num >= 2 and len(data_list) > 1:
        idx = int((mat1[k][count_num]) - 2)
        kclass[count_num - 1] = float(data_list[idx])
        k = int((mat1[k][count_num] - 1))
        count_num -= 1
    return kclass


def classify(addresses):
    data = []
    for address in addresses:
        data.append(address['mean'])

    breaks = get_jenks_breaks(data, 3)
    all_tuples = []
    print('BREAKS')
    print(breaks)
    if len(breaks) == 4:
        for num in addresses:
            mean = float(num['mean'])
            if mean >= breaks[0] and mean <= breaks[1]:
                num['rating'] = 'Good'
                all_tuples.append(num)
                # my_tuple = (num , 'Good')
                # all_tuples.append(my_tuple)
                #print(my_tuple)
            elif mean >= breaks[1] and mean <= breaks[3]:
                num['rating'] = 'Fair'
                all_tuples.append(num)
                # my_tuple = (num , 'Fair')
                # all_tuples.append(my_tuple)
                #print(my_tuple)
            else:
                num['rating'] = 'Bad'
                all_tuples.append(num)
                # my_tuple = (num , 'Bad')
                # all_tuples.append(my_tuple)
                #print(my_tuple)
    return all_tuples
