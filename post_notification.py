from sqlalchemy import create_engine, text, URL
from datetime import datetime, date
import os
import json

url_object = URL.create(
    os.environ["DATABASE_TYPE"],
    username=os.environ["USER_NAME"],
    password=os.environ["PASSWORD"],
    host=os.environ["HOST"],
    port=os.environ["PORT"],
    database=os.environ["DATABASE_NAME"],
)
engine = create_engine(
    url_object,
    echo=True,
)
cors_headers = {
    "Access-Control-Allow-Headers": "Content-Type,Authorization",
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "GET",
}


def lambda_handler(event, context):
    try:
        stmt = text(
            """
            UPDATE notification
            SET read = TRUE WHERE user_id = :id
            """
        )
        with engine.connect() as conn:
            result = conn.execute(
                stmt,
                {
                    "id": event["pathParameters"]["userId"],
                },
            )
            conn.commit()

    except Exception as error:
        print(error)
        return {
            "statusCode": "500",
            "headers": cors_headers,
            "body": json.dumps({"status": "error", "message": "Internal Server error"}),
        }
    else:
        return {
            "statusCode": "200",
            "headers": cors_headers,
            "body": json.dumps(
                {
                    "status": "success",
                    "message": "Notifications marked as read",
                }
            ),
        }
