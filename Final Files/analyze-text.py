import json
import boto3

def lambda_handler(event, context):
    comprehend = boto3.client(service_name='comprehend', region_name='us-east-1')

    # Identify sentiment
    sentiment_data = json.loads(json.dumps(comprehend.detect_sentiment(Text=event["text"], LanguageCode='en'), sort_keys=True, indent=4))
    sentiment = sentiment_data['Sentiment']
    
    # print(sentiment)
    print(sentiment_data)
    
    # response = {
    #     'statusCode': 200,
    #     'body': json.dumps(sentiment_data)
    # }
    
    # return response

    # Identify key phrases
    KP_data = json.loads(json.dumps(comprehend.detect_key_phrases(Text=event["text"], LanguageCode='en'), sort_keys=True, indent=4))
    KP = KP_data['KeyPhrases']
    KPList = []
    for phrase in KP:
        KPList.append(phrase['Text'])

    # Identify named entities
    NE_data = json.loads(json.dumps(comprehend.detect_entities(Text=event["text"], LanguageCode='en'), sort_keys=True, indent=4))
    NE = NE_data['Entities']
    
    # Identify the intent
    # Change the EndpointArn variable to use a different endpoint, or make it configurable
    text = event["text"]
    intent = comprehend.classify_document(
        Text = text,
        EndpointArn = 'arn:aws:comprehend:us-east-1:301251195635:document-classifier-endpoint/bank-test-endpoint'
        )
    
    data = json.dumps({'sentiment': sentiment, 'keyPhrases': KPList, 'namedEntities': NE, 'intent': intent})
    data = json.loads(data)
    
    
    return data
