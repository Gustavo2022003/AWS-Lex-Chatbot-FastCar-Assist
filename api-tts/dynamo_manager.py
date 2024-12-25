import boto3

class DynamoManager:
    def __init__(self, table_name):
        self.table = boto3.resource('dynamodb').Table(table_name)

    def get_phrase(self, text):
        response = self.table.scan(
            FilterExpression='received_phrase = :text',
            ExpressionAttributeValues={':text': text}
        )
        return response['Items']

    def save_phrase(self, unique_id, text, audio_url, timestamp):
        self.table.put_item(
            Item={
                "id": unique_id,
                "received_phrase": text,
                "audio_url": audio_url,
                "created_audio": timestamp,
            }
        )