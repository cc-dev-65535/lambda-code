import boto3
import os
import json
import uuid

s3_client = boto3.client("s3")
bucket = os.environ["BUCKET"]


def lambda_handler(event, context):
    for record in event["Records"]:
        body_dict = json.loads(record["body"])
        message_dict = json.loads(body_dict["Message"])
        log_dict = {
            "timestamp": body_dict["Timestamp"],
            "name": message_dict.get("name", ""),
            "email": message_dict.get("emails", []),
            "subject": body_dict["Subject"],
            "message": message_dict["body"],
        }
        response = s3_client.put_object(
            Body=json.dumps(log_dict),
            Bucket=bucket,
            Key=f"log/file-{str(uuid.uuid4())}.json",
            ContentType="application/json",
        )
