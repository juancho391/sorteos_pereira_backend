import os

import boto3
from dotenv import load_dotenv

load_dotenv()

s3 = boto3.client(
    "s3",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=os.getenv("AWS_S3_REGION_NAME"),
)

BUCKET_NAME = os.getenv("AWS_STORAGE_BUCKET_NAME")


def upload_image(file, folder="rifa_images"):
    try:
        s3.upload_fileobj(
            file.file,
            BUCKET_NAME,
            f"{folder}/{file.filename}",
            ExtraArgs={"ContentType": "image/png"},
        )

        file_url = f"https://{BUCKET_NAME}.s3.amazonaws.com/{folder}/{file.filename}"
        return file_url
    except Exception as e:
        return {"message": str(e)}
