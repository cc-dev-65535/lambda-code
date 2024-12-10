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
        print(event["queryStringParameters"])
        print(event["pathParameters"]["id"])
        stmt = text(
            """SELECT
                T.*, E.first_name, E.last_name, P.name AS project_name
                FROM timesheet T
                INNER JOIN project P
                ON T.project_id = P.id
                INNER JOIN "user" E
                ON T.employee_id = E.id
                WHERE P.id = :pid AND T.submission_date IS NOT NULL
                AND T.start_date_of_the_week = :sd AND (T.status = 'pending' OR T.status = 'approved')
                ORDER BY E.first_name, E.last_name
                """
        )
        with engine.connect() as conn:
            result = conn.execute(
                stmt,
                {
                    "pid": event["pathParameters"]["id"],
                    "sd": event["queryStringParameters"]["start_date"],
                },
            )

        data = [dict(row) for row in result.mappings().all()]
        formatted_data = list(
            map(
                lambda x: dict(
                    x,
                    id=str(x["id"]),
                    employee_id=str(x["employee_id"]),
                    project_id=str(x["project_id"]),
                    submission_date=(
                        x["submission_date"].isoformat()
                        if x["submission_date"]
                        else None
                    ),
                    approved_date=(
                        x["approved_date"].isoformat() if x["approved_date"] else None
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
