import json
from tts_service import TTSService
import logging
from utils import lexResponse

# Environment variables
TABLE_NAME = "Compass"
BUCKET_NAME = "bucket-tts-sls-ferrari"

# TTS Service Instance
tts_service = TTSService(TABLE_NAME, BUCKET_NAME)

# Health check function
def health(event, context):
    body = {
        "message": "Go Serverless v3.0! Your function executed successfully!",
        "input": event,
    }

    response = {"statusCode": 200, "body": json.dumps(body)}

    return response

# Show API's version
def v1_description(event, context):
    body = {"message": "TTS API version 1."}

    response = {"statusCode": 200, "body": json.dumps(body)}

    return response

def text_to_speech(event, context):
    try:
        body = json.loads(event["body"])
        text = body.get("received_phrase")

        if not text:
            return {
                "statusCode": 400,
                "body": json.dumps({"message": "received_phrase is required"}),
            }

        # Generate/recover the audio and text processing
        result = tts_service.process_text_to_speech(text)

        return {
            "statusCode": 200,
            "body": json.dumps(result),
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"message": str(e)})
        }

def lex_bot(event, context):
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # Debug
    logger.info(f'Evento recebido: {event}')

    intentName = event['sessionState']['intent']['name']
    slots = event['sessionState']['intent']['slots']

    response = lexResponse(intentName, slots)

    ttsEvent = {
        "body": json.dumps({'received_phrase': response['phrase']})
    }

    context = {}

    ttsResponse = text_to_speech(ttsEvent, context)
    ttsReponseBody = json.loads(ttsResponse.get('body', "{}"))

    s3Audio = ttsReponseBody.get('url_to_audio', '')

    lex_response = {
        "sessionState": {
            "sessionAttributes": event.get('sessionAttributes', {}),
            "dialogAction": {
                "type": "Close",
            },
            "intent": {
                "name": intentName,
                "state": "Fulfilled"
            }
        },
        "messages": [
            {
                "contentType": "PlainText",
                "content": response['phrase']
            },
            {
                "contentType": "PlainText",
                "content": f"Escutar a resposta: {s3Audio}"
            }
        ]
    }

    return lex_response