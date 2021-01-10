from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential
from discord import client

key = "85c6af76f9284d2b90f54e1e3317eed5"
endpoint = "https://nwhacks2021sentiment.cognitiveservices.azure.com/"


def authenticate_client():
    ta_credential = AzureKeyCredential(key)
    text_analytics_client = TextAnalyticsClient(
        endpoint=endpoint,
        credential=ta_credential)
    return text_analytics_client


# azure_client = authenticate_client()


def sentiment_analysis(client, statement):

    # array of strings - response = client.analyze_sentiment(documents=documents)
    # need to divide array of strings to one string at a time
    # this will determine what sentiment is - <string>.sentiment
    # sentence.confidence_scores.positive
    # sentence.confidence_scores.neutral
    # sentence.confidence_scores.negative
    response = client.analyze_sentiment(documents=statement)[0]
    return(response.sentiment)

    # array of strings - response = client.analyze_sentiment(documents=documents)
    # need to divide array of strings to one string at a time
    # this will determine what sentiment is - <string>.sentiment
    # sentence.confidence_scores.positive
    # sentence.confidence_scores.neutral
    # sentence.confidence_scores.negative


def sentiment_confidence(client, statement):

    response = client.analyze_sentiment(documents=statement)[0]
    return([float(response.confidence_scores.positive), float(response.confidence_scores.neutral), float(response.confidence_scores.negative)])


# def sentiment_analysis_example(client):

#     documents = [
#         "I had the best day of my life. I wish you were there with me."]
#     response = client.analyze_sentiment(documents=documents)[0]
#     print("Document Sentiment: {}".format(response.sentiment))
#     print("Overall scores: positive={0:.2f}; neutral={1:.2f}; negative={2:.2f} \n".format(
#         response.confidence_scores.positive,
#         response.confidence_scores.neutral,
#         response.confidence_scores.negative,
#     ))
#     for idx, sentence in enumerate(response.sentences):
#         print("Sentence: {}".format(sentence.text))
#         print("Sentence {} sentiment: {}".format(idx+1, sentence.sentiment))
#         print("Sentence score:\nPositive={0:.2f}\nNeutral={1:.2f}\nNegative={2:.2f}\n".format(
#             sentence.confidence_scores.positive,
#             sentence.confidence_scores.neutral,
#             sentence.confidence_scores.negative,
#         ))


# sentiment_analysis_example(azure_client)
