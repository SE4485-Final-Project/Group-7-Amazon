import json
import boto3

client = boto3.client("lambda")

def lambda_handler(event, context):
    
    
    input = {
  "recordType": "GET",
  "data": {
    "tableName": "demo",
    "id": "Lexmark"
  }
};
    response = client.invoke(FunctionName='arn:aws:lambda:us-east-1:301251195635:function:DynamoDBHandler',
    InvocationType ='RequestResponse',
    Payload = json.dumps(input))
    
    responseJson = json.load(response['Payload'])
    
    return(responseJson)
