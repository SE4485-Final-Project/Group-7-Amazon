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

    recordType = event["recordType"]
    data = event["data"]
    if(recordType == "ADD"):
        _tn = data["tableName"]
        Intent = data["Intent"]
        Sentiment = data["Sentiment"]
        Sentence = data["Sentence"]
        Time = data["Time"]
        Type = data["Type"]
        fn = data["FirstName"]
        response = add_item(client,_tn,Intent,Sentiment,Sentence,Time,Type, fn)
    return deserialize(response)
        
