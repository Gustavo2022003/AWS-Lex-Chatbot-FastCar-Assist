import boto3

class S3Manager:
    def __init__(self, bucket_name):
        self.s3 = boto3.client('s3')
        self.bucket_name = bucket_name

    def upload_audio(self, file_name, audio_stream):
        self.s3.put_object(
            Bucket=self.bucket_name,
            Key=file_name,
            Body=audio_stream,
            ContentType="audio/mpeg"
        )

    def get_audio_url(self, file_name):
        return f"https://{self.bucket_name}.s3.amazonaws.com/{file_name}"
