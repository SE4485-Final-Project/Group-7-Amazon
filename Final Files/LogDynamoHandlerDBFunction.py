from botocore.exceptions import ClientError
import boto3
import uuid

def add_item(client,_tableName,Intent,Sentiment,Sentence,Time,Type, FN):
    
    response = client.put_item(
        TableName = _tableName,
        Item ={
             "UniqueID": {
              "S": str(uuid.uuid4())
             },
             "Intent": {
              "S": Intent
             },
             "Sentiment": {
              "S": Sentiment
             },
             "Sentence": {
              "S": Sentence
             },
             "Time": {
              "S": Time
             },
             "Type": {
              "S": Type
             },
             "FirstName": {
              "S": FN
             }
        }
    )
    return response
