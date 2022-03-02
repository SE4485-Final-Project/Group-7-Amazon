from botocore.exceptions import ClientError
import boto3

def add_item(client,_tableName,_id,_type,_link):
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
def get_item(client,_tableName,_id):
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
