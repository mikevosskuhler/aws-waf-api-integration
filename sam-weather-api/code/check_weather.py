import boto3
import json
import urllib3
import os

client = boto3.client('ssm')
http = urllib3.PoolManager()

def handler(Event, Context):
    history_bucket = os.environ['history_bucket']
    key_name = os.environ['key']
    key = client.get_parameter(Name = key_name, WithDecryption = True)['Parameter']['Value']
    response = http.request('GET', f'api.openweathermap.org/data/2.5/weather?q=amersfoort&appid={key}')
    data = response.data

    return {
        "statusCode": 200,
        'body': data
    } 