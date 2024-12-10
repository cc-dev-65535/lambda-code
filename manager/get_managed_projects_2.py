from sqlalchemy import create_engine, text, URL
from datetime import datetime, date, timedelta
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


def subtract_time(end_time, start_time):
    end_time = datetime.strptime(end_time, "%H:%M")
    start_time = datetime.strptime(start_time, "%H:%M")
    return (end_time - start_time).total_seconds() / 3600


def lambda_handler(event, context):
    try:
        json_body = json.loads(event["body"])
        print(json_body)
        stmt_select_projects = text(
            f"""SELECT P.*
            FROM project P, "user" E
            WHERE P.project_manager_id = E.id AND E.id = :id"""
        )
        stmt_select_timesheets = text(
            """SELECT
                TR.start_time, TR.end_time
                FROM timesheet T
                INNER JOIN time_record TR
                ON T.id = TR.timesheet_id
                WHERE T.project_id = :pid
                AND T.submission_date IS NOT NULL AND T.status = 'approved'
                """
        )
        with engine.connect() as conn:
            result_select_projects = conn.execute(
                stmt_select_projects,
                {
                    "id": json_body["id"],
                },
            )
            select_data = [dict(row) for row in result_select_projects.mappings().all()]
            for row in select_data:
                result_select_timesheets = conn.execute(
                    stmt_select_timesheets,
                    {
                        "pid": row["id"],
                    },
                )
                row["approved_hours"] = [
                    dict(row) for row in result_select_timesheets.mappings().all()
                ]

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
                    approved_hours=sum(
                        [
                            subtract_time(record["end_time"], record["start_time"])
                            for record in x["approved_hours"]
                        ],
                        0,
                    ),
                ),
                select_data,
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
