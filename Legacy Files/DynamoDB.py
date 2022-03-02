from pprint import pprint
import boto3
import json
from botocore.exceptions import ClientError
from boto3.dynamodb.types import TypeDeserializer

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


data_j = open("local.json")
data_o = json.load(data_j)

client = boto3.client('dynamodb',aws_access_key_id=data_o["_ACCESSKEY"], aws_secret_access_key=data_o["_SECRETKEY"],region_name = "us-east-1")


#GET an ITEM from specific table using ID.
def get_item( _tableName,_id):
    try:
        response = client.get_item(
            TableName=_tableName,
            Key={
                'ID': {
                'S': _id
                }
            }
            # For conditions
            # ConditionExpression="size(info.actors) > :num",
            # ExpressionAttributeValues={':num': actor_count},

        )

    
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        if ("Item" in response):
            return response['Item']
        else :
            return "Key not found"

#ADD an ITEM to specific table using ID, TYPE, LINK
def add_item(_tableName,_id,_type,_link):
    response = client.put_item(
        TableName = _tableName,
        Item ={
            'ID': {
                'S': _id
            },
            'S_Type': {
                'S': _type
            },
            'Link':{
                'S':  _link
            }
        }
    )
    return response

#UPDATE an ITEM from a specifc table using ID, TYPE, LINK
def update_item(_tableName, _id, _type, _link):

    try:
        response = client.update_item(
            TableName = _tableName,
            Key={
                'ID': {
                    'S': _id
                }
            },

            UpdateExpression="set S_Type=:t, Link=:l",
            ConditionExpression="ID = :id",
            ExpressionAttributeValues={
                ':t': {'S': _type},
                ':l': {'S': _link},
                ':id':{'S': _id}
            },
            ReturnValues="UPDATED_NEW"
        )
    except ClientError as e:
        if e.response['Error']['Code'] == "ConditionalCheckFailedException":
            print(e.response['Error']['Message'])
        else:
            raise
    else:
        return response

#REMOVE an ITEM from a specific table using ID
def remove_item(_tableName, _id):
    try:
        response = client.delete_item(
            TableName = _tableName,
            Key={
                'ID': {
                    'S': _id
                }
            }
        )
    except ClientError as e:
        if e.response['Error']['Code'] == "ConditionalCheckFailedException":
            print(e.response['Error']['Message'])
        else:
            raise
    else:
        return response

#PRINTING a given table
def print_table(_tableName):
    items = client.scan(
        TableName = _tableName
    )["Items"]

    for i in items:
        print(i)


if __name__ == '__main__':

    add_item("demo","Rice Cooker", "Appliances" , "google.com")
    print_table("demo")
    
