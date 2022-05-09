from botocore.exceptions import ClientError
import boto3

def get_item(client,_tableName,_id):
    try:
        response = client.get_item(
            TableName=_tableName,
            Key={
                "Name": {
                "S": _id
                }
            }
        )
    
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        if ("Item" in response):
            return response['Item']
        else :
            return "Key not found"
