import boto3
import uuid
from botocore.client import ClientError
from fastapi import File, HTTPException
from config.settings import settings


class S3_CLIENT:

    def __init__(self):
        self.bucket_name = settings.AWS_BUCKET_NAME
        self.access_key = settings.AWS_ACCESS_KEY
        self.secret_key = settings.AWS_SECRET_KEY
        self.region = settings.AWS_REGION
        self.s3_client: boto3 = boto3.client(
            "s3", self.region, self.access_key, self.secret_key
        )
    

    async def upload_product_photo(self, file):
        random_prefix = str(uuid.uuid4())
        s3_key = f"product_images/{random_prefix}_{file.filename}"

        try:
            file.file.seek(0)
            self.s3_client.upload_fileobj(file.file, self.bucket_name, s3_key)
            db_key = f"https://s3.us-east-1.amazonaws.com/qamqor.kz-bucket/{s3_key}"
            return db_key
        except ClientError as e:
            raise HTTPException(
                status_code=500, detail=f"Failed to upload file: {str(e)}"
            )



aws_client = S3_CLIENT()
