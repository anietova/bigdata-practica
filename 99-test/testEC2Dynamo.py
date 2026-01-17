# test dynamo desde el EC2 donde está el productor
import boto3
from decimal import Decimal

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('trades')

response = table.scan(Limit=5)
for item in response['Items']:
    for k,v in item.items():
        if isinstance(v, Decimal):
            item[k] = float(v)
    print(item)