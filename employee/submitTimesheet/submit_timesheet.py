from sqlalchemy import create_engine, text, URL
from datetime import datetime, date
import boto3
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
    "Access-Control-Allow-Methods": "PATCH",
}

topic = os.environ["TOPIC_ARN"]
sns_client = boto3.client("sns")


class SubmissionException(Exception):
    pass


def lambda_handler(event, context):
    try:
        json_body = json.loads(event["body"])
        print(json_body)
        stmt_select = text(
            """SELECT *
            FROM timesheet
            WHERE id = :id"""
        )
        stmt_patch = text(
            """UPDATE timesheet
            SET submission_date = :sd, status = 'pending'
            WHERE id = :id"""
        )
        stmt_select_email = text(
            """SELECT
                P.name, E.email, E.first_name, E.last_name, T.start_date_of_the_week, E.id AS employee_id, T.project_id
                FROM timesheet T
                INNER JOIN project P
                ON T.project_id = P.id
                INNER JOIN "user" E
                ON P.project_manager_id = E.id
                WHERE T.id = :id"""
        )
        stmt_notification = text(
            """INSERT INTO notification (user_id, type, start_date_of_the_week, project_id)
            VALUES (:uid, 'submitted', :sd, :pid)"""
        )
        with engine.connect() as conn:
            result_select = conn.execute(
                stmt_select,
                {
                    "id": json_body["id"],
                },
            )

            for row in result_select:
                if row.status is not None and row.status != "rejected":
                    raise SubmissionException

            result_patch = conn.execute(
                stmt_patch,
                {
                    "id": json_body["id"],
                    "sd": json_body["submission_date"],
                },
            )

            result_select_email = conn.execute(
                stmt_select_email,
                {"id": json_body["id"]},
            )

            result_dicts = [dict(row) for row in result_select_email.mappings().all()]

            result_insert = conn.execute(
                stmt_notification,
                {
                    "uid": result_dicts[0]["employee_id"],
                    "sd": result_dicts[0]["start_date_of_the_week"],
                    "pid": result_dicts[0]["project_id"],
                },
            )
            conn.commit()

        response = sns_client.publish(
            TopicArn=topic,
            Message=json.dumps(
                {
                    "emails": [result_dicts[0]["email"]],
                    "name": result_dicts[0].get("first_name", "")
                    + " "
                    + result_dicts[0].get("last_name", ""),
                    "body": f"""We would like to notify you of a timesheet submission for project: <b>{result_dicts[0]["name"]}</b>,
                    on the week of <b>{result_dicts[0]['start_date_of_the_week']}</b>.""",
                }
            ),
            Subject="Timesheet submitted",
        )

    except SubmissionException:
        return {
            "statusCode": "200",
            "headers": cors_headers,
            "body": json.dumps(
                {"status": "success", "message": "Timesheet already submitted"}
            ),
        }
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
            "body": json.dumps({"status": "success", "message": "Timesheet submitted"}),
        }
