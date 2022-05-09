import json
import boto3
import datetime
import urllib3

client = boto3.client("lambda")

def logHandler(currentType, I = "", St = "", Sc = "", FN = ""):
    logType = currentType
    currentTime = datetime.datetime.now()
    
    db_input = {
      "recordType": "ADD",
      "data": {
        "tableName": "LogsTable",
        "Intent": I,
        "Sentiment": St,
        "Sentence": Sc,
        "Time": str(currentTime),
        "Type": logType, 
        "FirstName" : FN
      }
    };
    response = client.invoke(FunctionName='arn:aws:lambda:us-east-1:301251195635:function:LogDynamoHandler',
    InvocationType ='RequestResponse',
    Payload = json.dumps(db_input))
    
    print(response)
    
def lambda_handler(event, context):
    

    
    
    # URL of the company's databases is hardcoded, but should be a parameter arriving from the front-end.
    URL = "https://460ddzxgc6.execute-api.us-east-1.amazonaws.com/default/ConfigDynamoHandler"
    
    
    ##################################################################
    
    PARAMS = {'id':"Threshold", "tableName":"ITHelper_Config", "recordType":"GET"}
    http = urllib3.PoolManager()
    db_output = http.request(
        "GET",
        URL,
        fields=PARAMS
    )
    db_output = json.loads(db_output.data)
    certainty_bar = db_output['Value']
    

    
    
    ##
    
    PARAMS = {'id':"NoDBEntry", "tableName":"ITHelper_Config", "recordType":"GET"}
    http = urllib3.PoolManager()
    db_output = http.request(
        "GET",
        URL,
        fields=PARAMS
    )
    db_output = json.loads(db_output.data)
    NoDBEntryText = db_output['Value']
    
    ##
    
    
    PARAMS = {'id':"BelowThresholdResponse", "tableName":"ITHelper_Config", "recordType":"GET"}
    http = urllib3.PoolManager()
    db_output = http.request(
        "GET",
        URL,
        fields=PARAMS
    )
    db_output = json.loads(db_output.data)
    BelowThresholdResponse = db_output['Value']
    
    
    ##
    
    PARAMS = {'id':"NegativeSentimentResponse", "tableName":"ITHelper_Config", "recordType":"GET"}
    http = urllib3.PoolManager()
    db_output = http.request(
        "GET",
        URL,
        fields=PARAMS
    )
    db_output = json.loads(db_output.data)
    NegativeSentimentResponse = db_output['Value']
    
    ##
    
    PARAMS = {'id':"DynamoDBHandlerAddress", "tableName":"ITHelper_Config", "recordType":"GET"}
    http = urllib3.PoolManager()
    db_output = http.request(
        "GET",
        URL,
        fields=PARAMS
    )
    db_output = json.loads(db_output.data)
    DynamoDBHandlerAddress = db_output['Value']
    
    ##
    PARAMS = {'id':"TextAnalyzeAddress", "tableName":"ITHelper_Config", "recordType":"GET"}
    http = urllib3.PoolManager()
    db_output = http.request(
        "GET",
        URL,
        fields=PARAMS
    )
    db_output = json.loads(db_output.data)
    TextAnalyzeAddress = db_output['Value']
        ##Getting Varibles from Config File.
    
    
    ###################################################################
  
    
    # Get SENTENCE From API
    
    user_text = event["user_text"]
    
    # user_text = event;
    #user_text = "I lost my credit card, what do I do?"

    # Send Sentence to SentenceAnalyzer and receive Intent, Sentiment
  
    
    text_analyze_input = {
        "text": user_text
    }

    response = client.invoke(FunctionName = TextAnalyzeAddress,
    InvocationType ='RequestResponse',
    Payload = json.dumps(text_analyze_input))
    
    
    text_analyze_response = json.load(response["Payload"])
    
    # print(text_analyze_response)
    
    
    intent = text_analyze_response['intent']
    #intent = "Password"
    
    intent_classes = intent['Classes']
    intent_highest_prob = intent_classes[0]
    intent_value = intent_highest_prob['Name']
    if(intent_highest_prob['Score'] <= certainty_bar):
        logHandler("Intent score below threshold", intent_value, "-1", user_text)
        return {
            'statusCode': 200,
            'body': json.dumps(BelowThresholdResponse)
        }
    
    #intent = "password"
    sentiment = text_analyze_response['sentiment']
    
    #Sentiment is BAD
    if(sentiment == 'NEGATIVE'):
        #Call customer service.
        logHandler("Negative Sentiment", intent_value, sentiment, user_text)
        return {
            'statusCode': 200,
            'body': json.dumps(NegativeSentimentResponse)
        }
    else:
    #Sentiment is OKAY
        #Get info from DB
        db_input = {
          "recordType": "GET",
          "data": {
            "tableName": "demo",
            "id": intent_value
          }
        };
        response = client.invoke(FunctionName=DynamoDBHandlerAddress,
        InvocationType ='RequestResponse',
        Payload = json.dumps(db_input))
    
        db_output = json.load(response['Payload'])
        
        #If info exists
        if(db_output):
            #Return link
            logHandler("Success", intent_value, sentiment, user_text, "Austin")
            return {
                'statusCode': 200,
                'body':(db_output['Link'])
            }
        #else
            #Customer Service.
        logHandler("No DB Entry found", intent_value, sentiment, user_text)
        return {
            'statusCode': 200,
            'body': json.dumps(NoDBEntryText)
        }
