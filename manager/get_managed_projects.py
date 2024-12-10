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
        json_body = json.loads(event["body"])
        print(json_body)
        stmt_select_projects = text(
            f"""SELECT P.*
            FROM project P, "user" E
            WHERE P.project_manager_id = E.id AND E.id = :id"""
        )
        with engine.connect() as conn:
            result_select_projects = conn.execute(
                stmt_select_projects,
                {
                    "id": json_body["id"],
                },
            )
        data = [dict(row) for row in result_select_projects.mappings().all()]
        formatted_data = list(
            map(
                lambda x: dict(
                    x,
                    id=str(x["id"]),
                    project_manager_id=str(x["project_manager_id"]),
                    start_date=(
                        x["start_date"].isoformat() if x["start_date"] else None
                    ),
                    end_date=(x["end_date"].isoformat() if x["end_date"] else None),
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
