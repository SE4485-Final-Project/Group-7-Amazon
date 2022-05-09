from pprint import pprint
import boto3
import json
from botocore.exceptions import ClientError
from boto3.dynamodb.types import TypeDeserializer
from DB_Functions import *

serializer = TypeDeserializer()

def deserialize(data):
    if isinstance(data, list):
        return [deserialize(v) for v in data]

    if isinstance(data, dict):
        try:
            return serializer.deserialize(data)
        except TypeError:
            return {k: deserialize(v) for k, v in data.items()}
    else:
        return data

client = boto3.client('dynamodb')

def lambda_handler(event, context):
    
    recordType = event["queryStringParameters"]["recordType"]
    if (recordType == "GET"):
        _tn = event["queryStringParameters"]["tableName"]
        _id = event["queryStringParameters"]["id"]
        response = get_item(client,_tn,_id)
        

    return deserialize(response)
        
