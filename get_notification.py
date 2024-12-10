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
            SELECT * FROM notification
            WHERE user_id = :id AND read = false
            ORDER BY created_at DESC
            """
        )
        with engine.connect() as conn:
            result = conn.execute(
                stmt,
                {
                    "id": event["pathParameters"]["userId"],
                },
            )
        data = [dict(row) for row in result.mappings().all()]
        ## data.sort(key=lambda x: x["created_at"], reverse=True)
        formatted_data = list(
            map(
                lambda x: dict(
                    x,
                    id=str(x["id"]),
                    user_id=str(x["user_id"]),
                    project_id=str(x["project_id"]) if x["project_id"] else None,
                    start_date_of_the_week=(
                        datetime.strptime(
                            x["start_date_of_the_week"], "%Y-%m-%d"
                        ).strftime("%Y-%m-%dT%H:%M:%SZ")
                    ),
                    created_at=(x["created_at"].isoformat()),
                ),
                data,
            )
        )
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
                    "data": formatted_data,
                }
            ),
        }
