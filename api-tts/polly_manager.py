import boto3

class PollyManager:
    def __init__(self):
        self.polly_client = boto3.client('polly')

    def synthesize_speech(self, text, voice_id='Vitoria'):
        response = self.polly_client.synthesize_speech(
            Text=text,
            OutputFormat='mp3',
            VoiceId=voice_id
        )
        return response['AudioStream'].read()