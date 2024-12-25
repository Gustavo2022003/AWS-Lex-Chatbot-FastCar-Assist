import uuid
import datetime
from dynamo_manager import DynamoManager
from s3_manager import S3Manager
from polly_manager import PollyManager

class TTSService:
    def __init__(self, table_name, bucket_name):
        self.dynamo_manager = DynamoManager(table_name)
        self.s3_manager = S3Manager(bucket_name)
        self.polly_manager = PollyManager()

    def process_text_to_speech(self, text):
        # Verify if the text already exist
        existing_items = self.dynamo_manager.get_phrase(text)
        if existing_items:
            existing_item = existing_items[0]
            return {
                "message": "Information retrieved successfully",
                "id": existing_item['id'],
                "url_to_audio": existing_item['audio_url']
            }

        # Generate unique ID
        unique_id = str(uuid.uuid4())
        timestamp = datetime.datetime.now().isoformat()

        # Generate audio using Polly
        audio_stream = self.polly_manager.synthesize_speech(text)

        # Audio file's name
        file_name = f"{unique_id}.mp3"

        # Audio upload on S3
        self.s3_manager.upload_audio(file_name, audio_stream)

        # Get audio URL
        audio_url = self.s3_manager.get_audio_url(file_name)

        # Save data on DynamoDB
        self.dynamo_manager.save_phrase(unique_id, text, audio_url, timestamp)

        return {
            "message": "Information saved successfully",
            "id": unique_id,
            "url_to_audio": audio_url
        }