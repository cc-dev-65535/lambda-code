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
    "Access-Control-Allow-Headers": "Content-Type",
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "GET",
}


def lambda_handler(event, context):
    try:
        print(event["pathParameters"]["projectId"])
        stmt = text(
            """SELECT
                P.*
                FROM project P
                WHERE P.id = :pid
                """
        )
        with engine.connect() as conn:
            result = conn.execute(
                stmt,
                {
                    "pid": event["pathParameters"]["projectId"],
                },
            )

        data = [dict(row) for row in result.mappings().all()]
        formatted_data = list(
            map(
                lambda x: dict(
                    x,
                    id=str(x["id"]),
                    project_manager_id=str(x["project_manager_id"]),
                    start_date=(
                        x["start_date"].strftime("%Y-%m-%d")
                        if x["start_date"]
                        else None
                    ),
                    end_date=(
                        x["end_date"].strftime("%Y-%m-%d") if x["end_date"] else None
                    ),
                ),
                data,
            )
        )

    except Exception as error:
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
