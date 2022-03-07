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

    input2 = {
        "text": "I want icecream?" 
    }

    response = client.invoke(FunctionName = 'arn:aws:lambda:us-east-1:479476530446:function:analyze-text',
    InvocationType ='RequestResponse',
    Payload = json.dumps(input2))
    
    compResponse = json.load(response["Payload"])
    #compResponse = compResponse.strip()
    #compResponse = compResponse[1:len(compResponse)-1]
    #compResponse = compResponse.replace('\\','')
    
    print(compResponse)
    
    _id = compResponse["keyPhrases"][0]

    input = {
      "recordType": "GET",
      "data": {
        "tableName": "demo",
        "id": _id
      }
    };
    response = client.invoke(FunctionName='arn:aws:lambda:us-east-1:301251195635:function:DynamoDBHandler',
    InvocationType ='RequestResponse',
    Payload = json.dumps(input))
    
    responseJson = json.load(response['Payload'])
    
    return(responseJson)
