import boto3
import json

def analyze_text(text):

    comprehend = boto3.client(service_name='comprehend', region_name='us-east-2')

    # Identify sentiment
    sentiment_data = json.loads(json.dumps(comprehend.detect_sentiment(Text=text, LanguageCode='en'), sort_keys=True, indent=4))
    sentiment = sentiment_data['Sentiment']

    # Identify key phrases
    KP_data = json.loads(json.dumps(comprehend.detect_key_phrases(Text=text, LanguageCode='en'), sort_keys=True, indent=4))
    KP = KP_data['KeyPhrases']
    KPList = []
    for phrase in KP:
        KPList.append(phrase['Text'])

    # Identify named entities
    #NE_json_str = json.dumps(comprehend.detect_entities(Text=text, LanguageCode='en'), sort_keys=True, indent=4)
    NE_data = json.loads(json.dumps(comprehend.detect_entities(Text=text, LanguageCode='en'), sort_keys=True, indent=4))
    NE = NE_data['Entities']
    #print (NE_json_str)
    #print(NE)

    return sentiment, KPList, NE


text = "Hello Zhang Wei, I am John. Your AnyCompany Financial Services, LLC credit card account 1111-0000-1111-0008 has " \
       "a minimum payment of $24.53 that is due by July 31st. Based on your autopay settings, we will withdraw your payment" \
       " on the due date from your bank account number XXXXXX1111 with the routing number XXXXX0000." \
       "Your latest statement was mailed to 100 Main Street, Any City, WA 98121." \
       "After your payment is received, you will receive a confirmation text message at 206-555-0100. " \
       "If you have questions about your bill, AnyCompany Customer Service is available by phone at 206-555-0199 or email at support@anycompany.com."

sentiment, key_phrases, named_entities = analyze_text(text)
print(sentiment)
print(key_phrases)
print(named_entities)