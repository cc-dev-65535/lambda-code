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
        print(event["pathParameters"]["id"])
        print(event["queryStringParameters"]["pid"])
        stmt = text(
            """SELECT
                TR.start_time, TR.end_time
                FROM timesheet T
                INNER JOIN "user" E
                ON T.employee_id = E.id
                INNER JOIN time_record TR
                ON TR.timesheet_id = T.id
                WHERE E.id = :id AND T.project_id = :pid
                AND T.submission_date IS NOT NULL AND T.status = 'approved'
                """
        )
        with engine.connect() as conn:
            result = conn.execute(
                stmt,
                {
                    "id": event["pathParameters"]["id"],
                    "pid": event["queryStringParameters"]["pid"],
                },
            )
        data = [dict(row) for row in result.mappings().all()]
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
                    "data": data,
                }
            ),
        }
